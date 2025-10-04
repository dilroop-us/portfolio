from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import time
import uuid
import asyncio
import httpx
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from backend.database import get_db
from backend.models import ContactMessage
from backend.schemas import (
    ContactMessageCreate, ContactMessageResponse, FullTextSearchRequest,
    FullTextSearchResponse, CircuitBreakerStatus, BackgroundTaskRequest,
    BackgroundTaskResponse, ProxyRequest, ProxyResponse
)
from backend.redis_client import redis_client
from backend.config import settings

router = APIRouter(prefix="/api", tags=["misc"])

circuit_breaker = None

def set_circuit_breaker(breaker):
    global circuit_breaker
    circuit_breaker = breaker

async def simulate_data_export(task_id: str, params: dict):
    await asyncio.sleep(2)
    if redis_client.is_connected():
        redis_client.set(f"task:{task_id}", {"status": "completed", "result": "Export finished"}, 3600)
    print(f"Task {task_id}: Data export completed")

async def simulate_report_generation(task_id: str, params: dict):
    await asyncio.sleep(3)
    if redis_client.is_connected():
        redis_client.set(f"task:{task_id}", {"status": "completed", "result": "Report generated"}, 3600)
    print(f"Task {task_id}: Report generation completed")

async def send_email_notification(name: str, email: str, message: str):
    if not settings.mail_username or not settings.mail_password:
        print(f"⚠️ Email not configured. Message from {name} ({email}): {message}")
        return
    
    try:
        from pydantic import SecretStr
        
        conf = ConnectionConfig(
            MAIL_USERNAME=str(settings.mail_username),
            MAIL_PASSWORD=SecretStr(str(settings.mail_password)),
            MAIL_FROM=str(settings.mail_from),
            MAIL_PORT=int(settings.mail_port),
            MAIL_SERVER=str(settings.mail_server),
            MAIL_STARTTLS=bool(settings.mail_starttls),
            MAIL_SSL_TLS=bool(settings.mail_ssl_tls),
            USE_CREDENTIALS=bool(settings.mail_use_credentials),
            MAIL_FROM_NAME=str(settings.mail_from_name)
        )
        
        email_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td align="center" style="padding: 40px 20px;">
                        <table role="presentation" style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">📬 New Contact Message</h1>
                                    <p style="margin: 8px 0 0 0; color: #cccccc; font-size: 14px;">Someone just reached out via your portfolio</p>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    <!-- Sender Info -->
                                    <div style="background-color: #f8f8f8; border-left: 4px solid #1a1a1a; padding: 20px; margin-bottom: 24px; border-radius: 4px;">
                                        <p style="margin: 0 0 12px 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">From</p>
                                        <p style="margin: 0 0 8px 0; color: #1a1a1a; font-size: 18px; font-weight: 600;">{name}</p>
                                        <p style="margin: 0; color: #666666; font-size: 14px;">
                                            <a href="mailto:{email}" style="color: #1a1a1a; text-decoration: none;">{email}</a>
                                        </p>
                                    </div>
                                    
                                    <!-- Message -->
                                    <div style="margin-bottom: 24px;">
                                        <p style="margin: 0 0 12px 0; color: #666666; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">Message</p>
                                        <div style="background-color: #f8f8f8; padding: 20px; border-radius: 4px;">
                                            <p style="margin: 0; color: #1a1a1a; font-size: 15px; line-height: 1.6; white-space: pre-wrap;">{message}</p>
                                        </div>
                                    </div>
                                    
                                    <!-- Action Button -->
                                    <div style="text-align: center; margin-top: 32px;">
                                        <a href="mailto:{email}?subject=Re: Your message via portfolio" 
                                           style="display: inline-block; background-color: #1a1a1a; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 6px; font-weight: 600; font-size: 14px;">
                                            Reply to {name.split()[0]}
                                        </a>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f8f8; padding: 20px 30px; text-align: center; border-radius: 0 0 8px 8px; border-top: 1px solid #e5e5e5;">
                                    <p style="margin: 0; color: #999999; font-size: 12px;">
                                        This message was sent from your portfolio contact form
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        message_schema = MessageSchema(
            subject=f"💬 {name} sent you a message",
            recipients=[settings.mail_to],
            body=email_body,
            subtype=MessageType.html
        )
        
        fm = FastMail(conf)
        await fm.send_message(message_schema)
        print(f"✅ Email sent successfully to {settings.mail_to}")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

@router.post("/contact", response_model=ContactMessageResponse)
async def create_contact(
    message: ContactMessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_message = ContactMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    background_tasks.add_task(
        send_email_notification,
        message.name,
        message.email,
        message.message
    )
    
    return db_message

@router.get("/contact", response_model=List[ContactMessageResponse])
async def get_messages(db: Session = Depends(get_db)):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return messages

@router.post("/search/fulltext", response_model=FullTextSearchResponse)
async def fulltext_search(request: FullTextSearchRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    if request.table not in ['products', 'users', 'customers']:
        raise HTTPException(status_code=400, detail="Invalid table")
    
    search_column = request.columns[0] if request.columns else 'name'
    
    query = text(f"""
        SELECT * FROM {request.table}
        WHERE to_tsvector('english', {search_column}) @@ plainto_tsquery('english', :search_term)
        LIMIT 20
    """)
    
    result = db.execute(query, {"search_term": request.search_term})
    results = [dict(row._mapping) for row in result]
    
    execution_time = (time.time() - start_time) * 1000
    
    return FullTextSearchResponse(
        results=results,
        total_count=len(results),
        search_term=request.search_term,
        execution_time=execution_time
    )

@router.get("/circuit-breaker/status", response_model=CircuitBreakerStatus)
async def get_circuit_breaker_status():
    return CircuitBreakerStatus(
        name="demo_service",
        state=str(circuit_breaker.current_state),
        failure_count=circuit_breaker.fail_counter,
        success_count=0,
        last_failure_time=None,
        next_retry_time=None
    )

@router.get("/circuit-breaker/call")
async def call_with_circuit_breaker():
    @circuit_breaker
    def risky_operation():
        import random
        if random.random() < 0.3:
            raise Exception("Service unavailable")
        return {"status": "success", "data": "Operation completed"}
    
    try:
        result = risky_operation()
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Circuit breaker: {str(e)}")

@router.post("/tasks/background", response_model=BackgroundTaskResponse)
async def create_background_task(request: BackgroundTaskRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
    if request.task_type == "data_export":
        background_tasks.add_task(simulate_data_export, task_id, request.params)
        return BackgroundTaskResponse(
            task_id=task_id,
            status="queued",
            message=f"Data export task queued with ID: {task_id}"
        )
    elif request.task_type == "report_generation":
        background_tasks.add_task(simulate_report_generation, task_id, request.params)
        return BackgroundTaskResponse(
            task_id=task_id,
            status="queued",
            message=f"Report generation task queued with ID: {task_id}"
        )
    else:
        raise HTTPException(status_code=400, detail="Unknown task type")

@router.get("/demo/posts")
async def get_demo_posts(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM demo_posts ORDER BY created_at DESC"))
    posts = []
    for row in result:
        posts.append({
            "id": row.id,
            "title": row.title,
            "body": row.body,
            "userId": row.user_id,
            "createdAt": row.created_at.isoformat() if row.created_at else None
        })
    return posts

@router.get("/demo/posts/{post_id}")
async def get_demo_post(post_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM demo_posts WHERE id = :id"), {"id": post_id})
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": row.id,
        "title": row.title,
        "body": row.body,
        "userId": row.user_id,
        "createdAt": row.created_at.isoformat() if row.created_at else None
    }

@router.post("/demo/posts")
async def create_demo_post(post_data: dict, db: Session = Depends(get_db)):
    title = post_data.get("title", "")
    body = post_data.get("body", "")
    user_id = post_data.get("userId", 1)
    
    result = db.execute(
        text("INSERT INTO demo_posts (title, body, user_id) VALUES (:title, :body, :user_id) RETURNING *"),
        {"title": title, "body": body, "user_id": user_id}
    )
    row = result.first()
    db.commit()
    
    if row:
        return {
            "id": row.id,
            "title": row.title,
            "body": row.body,
            "userId": row.user_id,
            "createdAt": row.created_at.isoformat() if row.created_at else None
        }
    return {"error": "Failed to create post"}

@router.get("/demo/users")
async def get_demo_users(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name, email FROM users LIMIT 10"))
    users = []
    for row in result:
        users.append({
            "id": row.id,
            "name": row.name,
            "email": row.email
        })
    return users

@router.post("/proxy", response_model=ProxyResponse)
async def proxy_request(proxy_req: ProxyRequest, request: Request):
    start_time = time.time()
    
    try:
        target_url = proxy_req.url
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = f"http://127.0.0.1:8000{target_url if target_url.startswith('/') else '/' + target_url}"
        
        headers = proxy_req.headers or {}
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.request(
                method=proxy_req.method,
                url=target_url,
                headers=headers,
                params=proxy_req.query_params,
                content=proxy_req.body.encode() if proxy_req.body else None
            )
            
            execution_time = time.time() - start_time
            
            response_headers = dict(response.headers)
            
            return ProxyResponse(
                status_code=response.status_code,
                headers=response_headers,
                body=response.text,
                execution_time=execution_time * 1000,
                error=None
            )
    
    except Exception as e:
        execution_time = time.time() - start_time
        return ProxyResponse(
            status_code=0,
            headers={},
            body="",
            execution_time=execution_time * 1000,
            error=str(e)
        )
