from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
import time
import random
import hashlib

from backend.database import get_db
from backend.redis_client import redis_client
from backend.quiz_questions import SQL_QUIZ_QUESTIONS

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

class QuizQuestion(BaseModel):
    id: int
    question: str
    difficulty: str
    points: int
    category: str

class QuizAnswerRequest(BaseModel):
    question_id: int
    user_query: str

class QuizAnswerResponse(BaseModel):
    correct: bool
    points_earned: int
    expected_query: Optional[str] = None
    user_result: Optional[list] = None
    expected_result: Optional[list] = None
    feedback: str

class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    score: int
    time_taken: int
    completed_at: str

class LeaderboardSubmission(BaseModel):
    username: str
    score: int
    time_taken: int

@router.get("/questions", response_model=List[QuizQuestion])
async def get_quiz_questions(count: int = 10, difficulty: Optional[str] = None):
    questions = SQL_QUIZ_QUESTIONS.copy()
    
    if difficulty:
        questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    
    random.shuffle(questions)
    selected_questions = questions[:min(count, len(questions))]
    
    return [
        QuizQuestion(
            id=q["id"],
            question=q["question"],
            difficulty=q["difficulty"],
            points=q["points"],
            category=q["category"]
        )
        for q in selected_questions
    ]

@router.post("/validate", response_model=QuizAnswerResponse)
async def validate_answer(request: QuizAnswerRequest, db: Session = Depends(get_db)):
    question = next((q for q in SQL_QUIZ_QUESTIONS if q["id"] == request.question_id), None)
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    user_query = request.user_query.strip()
    expected_query = question["expected_query"].strip()
    
    if not user_query.lower().startswith('select'):
        return QuizAnswerResponse(
            correct=False,
            points_earned=0,
            feedback="Only SELECT queries are allowed in the quiz."
        )
    
    try:
        user_result = db.execute(text(user_query))
        user_rows = [dict(row._mapping) for row in user_result.fetchall()]
        
        expected_result = db.execute(text(expected_query))
        expected_rows = [dict(row._mapping) for row in expected_result.fetchall()]
        
        def normalize_result(rows):
            if not rows:
                return []
            return sorted([
                {k: (str(v) if v is not None else None) for k, v in row.items()}
                for row in rows
            ], key=lambda x: str(sorted(x.items())))
        
        user_normalized = normalize_result(user_rows)
        expected_normalized = normalize_result(expected_rows)
        
        is_correct = user_normalized == expected_normalized
        
        if is_correct:
            return QuizAnswerResponse(
                correct=True,
                points_earned=question["points"],
                user_result=user_rows[:5],
                expected_result=expected_rows[:5],
                feedback=f"Correct! You earned {question['points']} points. Great job!"
            )
        else:
            return QuizAnswerResponse(
                correct=False,
                points_earned=0,
                expected_query=expected_query,
                user_result=user_rows[:5],
                expected_result=expected_rows[:5],
                feedback="Incorrect. The results don't match. Check the expected query and try again."
            )
    
    except Exception as e:
        return QuizAnswerResponse(
            correct=False,
            points_earned=0,
            expected_query=expected_query,
            feedback=f"Query error: {str(e)}"
        )

@router.post("/leaderboard/submit")
async def submit_score(submission: LeaderboardSubmission):
    if not redis_client.is_connected():
        raise HTTPException(status_code=503, detail="Leaderboard service unavailable")
    
    if not submission.username or len(submission.username) < 2:
        raise HTTPException(status_code=400, detail="Username must be at least 2 characters")
    
    if submission.score < 0 or submission.score > 3300:
        raise HTTPException(status_code=400, detail="Invalid score")
    
    try:
        leaderboard_key = "sql_quiz_leaderboard"
        user_key = f"quiz_user:{submission.username.lower()}"
        
        existing_score = redis_client.redis.zscore(leaderboard_key, submission.username.lower())
        
        if existing_score is None or submission.score > existing_score:
            redis_client.redis.zadd(leaderboard_key, {submission.username.lower(): submission.score})
            
            redis_client.redis.hset(user_key, mapping={
                "username": submission.username,
                "score": submission.score,
                "time_taken": submission.time_taken,
                "completed_at": str(time.time())
            })
            redis_client.redis.expire(user_key, 86400 * 30)
            
            return {"success": True, "message": "Score submitted successfully", "new_record": existing_score is None or submission.score > existing_score}
        else:
            return {"success": True, "message": "Score recorded but not a new personal best", "new_record": False}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit score: {str(e)}")

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 10):
    if not redis_client.is_connected():
        return []
    
    try:
        leaderboard_key = "sql_quiz_leaderboard"
        top_scores = redis_client.redis.zrevrange(leaderboard_key, 0, limit - 1, withscores=True)
        
        leaderboard = []
        for rank, (username_lower, score) in enumerate(top_scores, start=1):
            user_key = f"quiz_user:{username_lower.decode() if isinstance(username_lower, bytes) else username_lower}"
            user_data = redis_client.redis.hgetall(user_key)
            
            if user_data and len(user_data) > 0:
                if isinstance(list(user_data.keys())[0], bytes):
                    user_data = {k.decode(): v.decode() for k, v in user_data.items()}
                
                leaderboard.append(LeaderboardEntry(
                    rank=rank,
                    username=user_data.get("username", "Anonymous"),
                    score=int(score),
                    time_taken=int(user_data.get("time_taken", 0)),
                    completed_at=user_data.get("completed_at", "")
                ))
            else:
                leaderboard.append(LeaderboardEntry(
                    rank=rank,
                    username=username_lower.decode() if isinstance(username_lower, bytes) else username_lower,
                    score=int(score),
                    time_taken=0,
                    completed_at=""
                ))
        
        return leaderboard
    
    except Exception as e:
        print(f"Leaderboard error: {str(e)}")
        return []

@router.get("/user-stats/{username}")
async def get_user_stats(username: str):
    if not redis_client.is_connected():
        return {"rank": None, "score": 0, "time_taken": 0}
    
    try:
        leaderboard_key = "sql_quiz_leaderboard"
        user_key = f"quiz_user:{username.lower()}"
        
        score = redis_client.redis.zscore(leaderboard_key, username.lower())
        if score is None:
            return {"rank": None, "score": 0, "time_taken": 0}
        
        rank = redis_client.redis.zrevrank(leaderboard_key, username.lower())
        user_data = redis_client.redis.hgetall(user_key)
        
        time_taken = 0
        if user_data and len(user_data) > 0:
            if isinstance(list(user_data.keys())[0], bytes):
                user_data = {k.decode(): v.decode() for k, v in user_data.items()}
            time_taken = int(user_data.get("time_taken", 0))
        
        return {
            "rank": rank + 1 if rank is not None else None,
            "score": int(score),
            "time_taken": time_taken
        }
    
    except Exception as e:
        return {"rank": None, "score": 0, "time_taken": 0}
