from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
import uuid
import asyncio
from collections import defaultdict
import time

from backend.database import get_db, SessionLocal
from backend.models import ChatSession, ChatMessage

router = APIRouter(prefix="/api/chat", tags=["chat"])

class SessionCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-zA-Z0-9_\s]+$')

class SessionResponse(BaseModel):
    token: str
    username: str
    expires_at: datetime

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class MessageResponse(BaseModel):
    id: int
    username: str
    content: str
    created_at: datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rate_limit: Dict[str, List[float]] = defaultdict(list)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                dead_connections.append(connection)
        
        for conn in dead_connections:
            self.disconnect(conn)

    def check_rate_limit(self, token: str, max_messages: int = 5, window: int = 10) -> bool:
        now = time.time()
        self.rate_limit[token] = [t for t in self.rate_limit[token] if now - t < window]
        
        if len(self.rate_limit[token]) >= max_messages:
            return False
        
        self.rate_limit[token].append(now)
        return True

manager = ConnectionManager()

@router.post("/session", response_model=SessionResponse)
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    username = session_data.username.strip()
    
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    token = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    session = ChatSession(
        id=session_id,
        username=username,
        token=token,
        expires_at=expires_at
    )
    
    db.add(session)
    db.commit()
    
    return SessionResponse(
        token=token,
        username=username,
        expires_at=expires_at
    )

@router.get("/history", response_model=List[MessageResponse])
async def get_message_history(limit: int = 200, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).order_by(
        ChatMessage.created_at.desc()
    ).limit(min(limit, 200)).all()
    
    return [
        MessageResponse(
            id=msg.id,
            username=msg.username,
            content=msg.content,
            created_at=msg.created_at
        ) for msg in reversed(messages)
    ]

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = ""):
    if not token:
        await websocket.close(code=1008, reason="Missing session token")
        return
    
    db = SessionLocal()
    
    try:
        session = db.query(ChatSession).filter(
            ChatSession.token == token
        ).first()
        
        if not session:
            await websocket.close(code=1008, reason="Invalid session token")
            return
        
        if session.expires_at < datetime.utcnow():
            await websocket.close(code=1008, reason="Session expired")
            return
        
        await manager.connect(websocket)
        
        session.last_active = datetime.utcnow()
        db.commit()
        
        while True:
            data = await websocket.receive_json()
            content = data.get('content', '').strip()
            
            if not content or len(content) > 500:
                await websocket.send_json({
                    "error": "Message must be between 1 and 500 characters"
                })
                continue
            
            if not manager.check_rate_limit(token):
                await websocket.send_json({
                    "error": "Rate limit exceeded. Please slow down."
                })
                continue
            
            message = ChatMessage(
                session_id=session.id,
                username=session.username,
                content=content,
                created_at=datetime.utcnow()
            )
            
            db.add(message)
            db.commit()
            db.refresh(message)
            
            session.last_active = datetime.utcnow()
            db.commit()
            
            await manager.broadcast({
                "id": message.id,
                "username": message.username,
                "content": message.content,
                "created_at": message.created_at.isoformat()
            })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
    finally:
        db.close()

@router.delete("/cleanup")
async def cleanup_expired_sessions(db: Session = Depends(get_db)):
    expired_sessions = db.query(ChatSession).filter(
        ChatSession.expires_at < datetime.utcnow()
    ).all()
    
    deleted_count = 0
    for session in expired_sessions:
        db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).delete()
        
        db.delete(session)
        deleted_count += 1
    
    db.commit()
    
    return {"deleted_sessions": deleted_count, "status": "success"}
