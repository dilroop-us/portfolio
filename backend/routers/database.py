from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import time
import hashlib
import sqlparse

from backend.database import get_db
from backend.schemas import (
    QueryRequest, QueryResponse, ExplainQueryRequest, QueryPlan,
    CachedQueryResponse, CachedQueryRequest, TransactionRequest,
    TransactionResponse, IndexRecommendation, QueryPlanVisualization,
    SQLInjectionDemo
)
from backend.redis_client import redis_client

router = APIRouter(prefix="/api", tags=["database"])

@router.post("/execute-query", response_model=QueryResponse)
async def execute_query(request: QueryRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    try:
        query_stripped = request.query.strip()
        query_lower = query_stripped.lower()
        
        first_word = query_lower.split()[0] if query_lower.split() else ''
        if first_word != 'select':
            return QueryResponse(
                success=False,
                error="Only SELECT queries are allowed. Query must start with SELECT.",
                execution_time=0
            )
        
        result = db.execute(text(query_stripped))
        rows = [dict(row._mapping) for row in result.fetchall()]
        
        execution_time = time.time() - start_time
        return QueryResponse(
            success=True,
            data=rows,
            execution_time=round(execution_time * 1000, 2)
        )
    except Exception as e:
        execution_time = time.time() - start_time
        error_message = str(e)
        if "no such table" in error_message.lower():
            error_message = f"Table not found. Available tables: users, customers, orders, products, employees"
        return QueryResponse(
            success=False,
            error=error_message,
            execution_time=round(execution_time * 1000, 2)
        )

@router.post("/db/analyze-query", response_model=QueryPlan)
async def analyze_query(request: ExplainQueryRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    query_stripped = request.query.strip()
    if not query_stripped.lower().startswith('select'):
        raise HTTPException(status_code=400, detail="Only SELECT queries can be analyzed")
    
    try:
        explain_query = f"EXPLAIN ANALYZE {query_stripped}"
        result = db.execute(text(explain_query))
        plan_lines = [row[0] for row in result.fetchall()]
        plan = "\n".join(plan_lines)
        
        execution_time = (time.time() - start_time) * 1000
        
        recommendations = []
        complexity_score = 0
        
        parsed = sqlparse.parse(query_stripped)[0]
        tokens = [token for token in parsed.tokens if not token.is_whitespace]
        
        if any("JOIN" in str(token).upper() for token in tokens):
            complexity_score += 2
            if "Seq Scan" in plan:
                recommendations.append("Consider adding indexes on JOIN columns to avoid sequential scans")
        
        if any("WHERE" in str(token).upper() for token in tokens):
            complexity_score += 1
            if "Seq Scan" in plan:
                recommendations.append("Add indexes on WHERE clause columns for better performance")
        
        if "GROUP BY" in query_stripped.upper():
            complexity_score += 2
            recommendations.append("Ensure GROUP BY columns are indexed for faster aggregation")
        
        if "ORDER BY" in query_stripped.upper():
            complexity_score += 1
            recommendations.append("Index ORDER BY columns to avoid expensive sort operations")
        
        if not recommendations:
            recommendations.append("Query looks well optimized!")
        
        return QueryPlan(
            plan=plan,
            execution_time_ms=round(execution_time, 2),
            recommendations=recommendations,
            complexity_score=min(complexity_score, 10)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/db/cached-query", response_model=CachedQueryResponse)
async def cached_query_execute(request: CachedQueryRequest, db: Session = Depends(get_db)):
    query_stripped = request.query.strip()
    
    if not query_stripped.lower().startswith('select'):
        return CachedQueryResponse(
            success=False,
            cached=False,
            execution_time=0,
            error="Only SELECT queries are allowed"
        )
    
    cache_key = f"query_cache:{hashlib.md5(query_stripped.encode()).hexdigest()}"
    
    cached_result = redis_client.get(cache_key) if redis_client.is_connected() else None
    
    if cached_result:
        return CachedQueryResponse(
            success=True,
            data=cached_result,
            cached=True,
            execution_time=0
        )
    
    start_time = time.time()
    try:
        result = db.execute(text(query_stripped))
        rows = [dict(row._mapping) for row in result.fetchall()]
        execution_time = (time.time() - start_time) * 1000
        
        if redis_client.is_connected():
            redis_client.set(cache_key, rows, request.cache_ttl)
        
        return CachedQueryResponse(
            success=True,
            data=rows,
            cached=False,
            execution_time=round(execution_time, 2)
        )
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        return CachedQueryResponse(
            success=False,
            cached=False,
            execution_time=round(execution_time, 2),
            error=str(e)
        )

@router.post("/db/transaction", response_model=TransactionResponse)
async def execute_transaction(request: TransactionRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    try:
        results = []
        for operation in request.operations:
            query = operation.get("query", "")
            if not query.lower().startswith('select'):
                raise HTTPException(status_code=400, detail="Only SELECT queries allowed in demo")
            
            result = db.execute(text(query))
            rows = [dict(row._mapping) for row in result.fetchall()]
            results.append({"query": query, "rows": len(rows), "data": rows[:5]})
        
        db.commit()
        execution_time = (time.time() - start_time) * 1000
        
        return TransactionResponse(
            success=True,
            results=results,
            execution_time=round(execution_time, 2)
        )
    except Exception as e:
        db.rollback()
        execution_time = (time.time() - start_time) * 1000
        return TransactionResponse(
            success=False,
            error=str(e),
            execution_time=round(execution_time, 2)
        )

@router.get("/db/index-recommendations")
async def get_index_recommendations(db: Session = Depends(get_db)):
    recommendations = []
    
    recommendations.append(IndexRecommendation(
        table="orders",
        columns=["customer_id", "order_date"],
        reason="Frequent JOINs on customer_id and filtering by order_date",
        impact="High - 40-60% query performance improvement",
        sql="CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);"
    ))
    
    recommendations.append(IndexRecommendation(
        table="products",
        columns=["category", "price"],
        reason="Common filtering by category and sorting by price",
        impact="Medium - 30-40% improvement on category searches",
        sql="CREATE INDEX idx_products_category_price ON products(category, price);"
    ))
    
    recommendations.append(IndexRecommendation(
        table="employees",
        columns=["department"],
        reason="GROUP BY department queries in analytics",
        impact="Medium - Faster aggregation queries",
        sql="CREATE INDEX idx_employees_department ON employees(department);"
    ))
    
    return recommendations

@router.post("/db/visualize-plan", response_model=QueryPlanVisualization)
async def visualize_query_plan(request: ExplainQueryRequest, db: Session = Depends(get_db)):
    if not request.query.strip().upper().startswith('SELECT'):
        raise HTTPException(status_code=400, detail="Only SELECT queries allowed")
    
    start_time = time.time()
    
    try:
        explain_query = f"EXPLAIN (FORMAT JSON, ANALYZE, BUFFERS) {request.query}"
        result = db.execute(text(explain_query))
        row = result.fetchone()
        if not row:
            raise Exception("No query plan returned")
        plan_data = row[0]
        
        execution_time = (time.time() - start_time) * 1000
        
        plan_tree = plan_data[0]["Plan"]
        total_cost = plan_tree.get("Total Cost", 0)
        
        recommendations = []
        if total_cost > 100:
            recommendations.append("Consider adding indexes on frequently filtered columns")
        if "Seq Scan" in str(plan_tree):
            recommendations.append("Sequential scan detected - index might help")
        
        return QueryPlanVisualization(
            query=request.query,
            plan_tree=plan_tree,
            total_cost=total_cost,
            execution_time_ms=execution_time,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo/sql-injection", response_model=SQLInjectionDemo)
async def sql_injection_demo(user_input: str, db: Session = Depends(get_db)):
    safe_query = "SELECT * FROM users WHERE name = :name LIMIT 5"
    unsafe_query = f"SELECT * FROM users WHERE name = '{user_input}' LIMIT 5"
    
    safe_result = []
    try:
        result = db.execute(text(safe_query), {"name": user_input})
        safe_result = [dict(row._mapping) for row in result]
    except:
        safe_result = []
    
    unsafe_result = []
    explanation = ""
    
    if "'" in user_input or "--" in user_input or ";" in user_input:
        explanation = f"UNSAFE: Input '{user_input}' contains SQL injection patterns. Safe query uses parameterization to prevent this."
        unsafe_result = [{"warning": "SQL injection attempt blocked in demo"}]
    else:
        try:
            result = db.execute(text(unsafe_query))
            unsafe_result = [dict(row._mapping) for row in result]
            explanation = "Input is safe. Both queries return the same result."
        except:
            explanation = "Unsafe query failed - demonstrating SQL injection vulnerability"
    
    return SQLInjectionDemo(
        query_type="User search by name",
        user_input=user_input,
        safe_query=safe_query,
        unsafe_query=unsafe_query,
        safe_result=safe_result,
        unsafe_result=unsafe_result,
        explanation=explanation
    )
