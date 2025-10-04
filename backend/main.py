from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import uuid
import time
from typing import Dict, Any
from collections import defaultdict
from cachetools import LRUCache
from pybreaker import CircuitBreaker

from backend.database import Base, engine
from backend.graphql.schema import schema
from backend.services.data_service import initialize_sample_data, check_rate_limit

from backend.routers import portfolio, database, auth, cache, misc, chat, quiz

db_connected = False
db_error = None

try:
    Base.metadata.create_all(bind=engine)
    db_connected = True
    print("✅ Database connected successfully")
except Exception as e:
    db_error = str(e)
    print(f"⚠️ Database connection failed: {e}")
    print("Backend will start anyway - database endpoints may fail")

l1_cache = LRUCache(maxsize=100)
l1_stats = {"hits": 0, "misses": 0}
l2_stats = {"hits": 0, "misses": 0}

circuit_breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

request_metrics: Dict[str, Dict[str, Any]] = defaultdict(
    lambda: {"count": 0, "total_time": 0.0, "errors": 0, "times": []}
)

app = FastAPI(title="Dilroop Portfolio API")

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache.set_cache_references(l1_cache, l1_stats, l2_stats)
misc.set_circuit_breaker(circuit_breaker)

app.include_router(portfolio.router)
app.include_router(database.router)
app.include_router(auth.router)
app.include_router(cache.router)
app.include_router(misc.router)
app.include_router(chat.router)
app.include_router(quiz.router)

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = str(process_time)
    
    endpoint = f"{request.method} {request.url.path}"
    request_metrics[endpoint]["count"] += 1
    request_metrics[endpoint]["total_time"] += process_time
    request_metrics[endpoint]["times"].append(process_time)
    if response.status_code >= 400:
        request_metrics[endpoint]["errors"] += 1
    
    return response

@app.on_event("startup")
async def startup_event():
    global db_connected
    if db_connected:
        try:
            initialize_sample_data()
            print("✅ Sample data initialized")
        except Exception as e:
            print(f"⚠️ Failed to initialize sample data: {e}")
    else:
        print("⚠️ Skipping data initialization - database not connected")

@app.get("/")
async def root():
    return {"message": "Welcome to Dilroop's Portfolio API", "status": "active"}

@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "database": {
            "connected": db_connected,
            "error": db_error if not db_connected else None
        }
    }

@app.get("/health/db")
async def database_health():
    if not db_connected:
        return {
            "status": "disconnected",
            "error": db_error,
            "message": "Database is not available. Please check your DATABASE_URL and ensure the database is running.",
            "troubleshooting": {
                "neon": "Go to console.neon.tech and enable/resume your endpoint",
                "digital_ocean": "Check your database cluster is active and IP is whitelisted"
            }
        }
    
    try:
        from backend.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {
            "status": "connected",
            "message": "Database is healthy and responding"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Database connection exists but queries are failing"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
