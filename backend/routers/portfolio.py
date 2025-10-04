from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Project, Skill, Challenge
from backend.schemas import ProjectResponse, SkillResponse, ChallengeResponse

router = APIRouter(prefix="/api", tags=["portfolio"])

@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    if not projects:
        default_projects = [
            Project(
                title="Smart Community Real-Time Data Platform",
                description="Designed a scalable, event-driven IoT backend for real-time data streaming from smart devices",
                tech_stack="Python,FastAPI,Django,PostgreSQL,Redis,AWS,Docker",
                year="2025",
                status="Production",
                throughput="30% improved efficiency",
                latency="20% reduced alert time",
                uptime="99.9%"
            ),
            Project(
                title="Multi-Seller E-commerce Platform",
                description="Developed a robust multi-seller e-commerce platform with RBAC, Stripe payments, and AWS deployment",
                tech_stack="Django,DRF,PostgreSQL,Redis,Stripe,AWS,Docker",
                year="2025",
                status="Production",
                throughput="500+ active users",
                latency="30% improved retrieval",
                uptime="99.5%"
            )
        ]
        db.add_all(default_projects)
        db.commit()
        projects = db.query(Project).all()
    return projects

@router.get("/skills", response_model=List[SkillResponse])
async def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    if not skills:
        default_skills = [
            Skill(name="Python", category="Languages", proficiency=95, years_experience=4),
            Skill(name="FastAPI", category="Frameworks", proficiency=90, years_experience=3),
            Skill(name="Django", category="Frameworks", proficiency=88, years_experience=3),
            Skill(name="PostgreSQL", category="Databases", proficiency=85, years_experience=3),
            Skill(name="Redis", category="Databases", proficiency=80, years_experience=2),
            Skill(name="SvelteKit", category="Frameworks", proficiency=85, years_experience=3),
            Skill(name="Docker", category="Tools", proficiency=82, years_experience=2),
            Skill(name="AWS", category="Tools", proficiency=78, years_experience=2),
        ]
        db.add_all(default_skills)
        db.commit()
        skills = db.query(Skill).all()
    return skills

@router.get("/challenges", response_model=List[ChallengeResponse])
async def get_challenges(db: Session = Depends(get_db)):
    challenges = db.query(Challenge).all()
    if not challenges:
        default_challenges = [
            Challenge(
                title="Basic Selection",
                difficulty="Beginner",
                description="Select all users from San Francisco",
                sql_solution="SELECT * FROM users WHERE city = 'San Francisco';",
                category="BASICS"
            ),
            Challenge(
                title="Age Filtering",
                difficulty="Beginner",
                description="Find all users older than 30 years",
                sql_solution="SELECT name, age, city FROM users WHERE age > 30;",
                category="BASICS"
            ),
            Challenge(
                title="Product Search",
                difficulty="Beginner",
                description="Find all electronics products under $100",
                sql_solution="SELECT * FROM products WHERE category = 'Electronics' AND price < 100;",
                category="BASICS"
            ),
            Challenge(
                title="Customer Orders Count",
                difficulty="Intermediate",
                description="Count how many orders each customer has made",
                sql_solution="SELECT c.name, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name;",
                category="JOINS"
            ),
            Challenge(
                title="Top Rated Products",
                difficulty="Intermediate",
                description="Find the top 3 highest-rated products",
                sql_solution="SELECT name, category, rating FROM products ORDER BY rating DESC LIMIT 3;",
                category="SORTING"
            ),
            Challenge(
                title="Average Order Value",
                difficulty="Intermediate",
                description="Calculate the average order amount for each customer",
                sql_solution="SELECT c.name, AVG(o.amount) as avg_order FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name;",
                category="AGGREGATION"
            ),
            Challenge(
                title="Department Salaries",
                difficulty="Intermediate",
                description="Find the total salary expense for each department",
                sql_solution="SELECT department, SUM(salary) as total_salary FROM employees GROUP BY department ORDER BY total_salary DESC;",
                category="AGGREGATION"
            ),
            Challenge(
                title="Manager Hierarchy",
                difficulty="Advanced",
                description="List all employees with their manager names",
                sql_solution="SELECT e.name as employee, m.name as manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;",
                category="JOINS"
            ),
            Challenge(
                title="Active Customer Revenue",
                difficulty="Advanced",
                description="Find total revenue from active customers with pending orders",
                sql_solution="SELECT c.name, SUM(o.amount) as pending_revenue FROM customers c JOIN orders o ON c.id = o.customer_id WHERE c.status = 'active' AND o.status = 'pending' GROUP BY c.id, c.name;",
                category="OPTIMIZATION"
            ),
            Challenge(
                title="Product Inventory Alert",
                difficulty="Advanced",
                description="Find products with stock below 100 and rating above 4.5",
                sql_solution="SELECT name, stock, rating, category FROM products WHERE stock < 100 AND rating > 4.5 ORDER BY stock ASC;",
                category="OPTIMIZATION"
            ),
            Challenge(
                title="City Demographics",
                difficulty="Advanced",
                description="Count users and calculate average age per city",
                sql_solution="SELECT city, COUNT(*) as user_count, AVG(age) as avg_age FROM users GROUP BY city ORDER BY user_count DESC;",
                category="AGGREGATION"
            ),
            Challenge(
                title="High Value Orders",
                difficulty="Advanced",
                description="Find customers who have orders over $500 and show order details",
                sql_solution="SELECT c.name as customer, o.amount, o.status FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.amount > 500 ORDER BY o.amount DESC;",
                category="JOINS"
            )
        ]
        db.add_all(default_challenges)
        db.commit()
        challenges = db.query(Challenge).all()
    return challenges

@router.get("/v1/projects", response_model=List[ProjectResponse])
async def get_projects_v1(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

@router.get("/v2/projects")
async def get_projects_v2(db: Session = Depends(get_db)):
    from datetime import datetime
    projects = db.query(Project).all()
    return {
        "version": "2.0",
        "data": [p.__dict__ for p in projects],
        "metadata": {
            "total": len(projects),
            "timestamp": datetime.utcnow().isoformat()
        }
    }
