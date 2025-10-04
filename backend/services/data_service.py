from sqlalchemy import text
from backend.database import SessionLocal

def initialize_sample_data():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"))
        if not result.scalar():
            db.execute(text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    age INTEGER,
                    city VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            db.execute(text("""
                INSERT INTO users (name, email, age, city) VALUES 
                ('John Doe', 'john@example.com', 28, 'San Francisco'),
                ('Jane Smith', 'jane@example.com', 32, 'New York'),
                ('Bob Johnson', 'bob@example.com', 45, 'Chicago'),
                ('Alice Williams', 'alice@example.com', 25, 'San Francisco'),
                ('Charlie Brown', 'charlie@example.com', 38, 'Seattle'),
                ('Emma Davis', 'emma@example.com', 29, 'Boston'),
                ('Michael Wilson', 'michael@example.com', 41, 'Austin'),
                ('Sarah Miller', 'sarah@example.com', 33, 'Portland')
            """))
            db.commit()
        
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'customers')"))
        if not result.scalar():
            db.execute(text("""
                CREATE TABLE customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    status VARCHAR(50),
                    total_spent DECIMAL(10,2)
                )
            """))
            db.execute(text("""
                CREATE TABLE orders (
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER REFERENCES customers(id),
                    amount DECIMAL(10,2),
                    status VARCHAR(50),
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            db.execute(text("""
                INSERT INTO customers (name, email, status, total_spent) VALUES 
                ('Alice Cooper', 'alice.c@email.com', 'active', 1250.00),
                ('Bob Smith', 'bob.s@email.com', 'active', 890.50),
                ('Charlie Davis', 'charlie.d@email.com', 'inactive', 340.00),
                ('Diana Prince', 'diana.p@email.com', 'active', 2100.00),
                ('Ethan Hunt', 'ethan.h@email.com', 'active', 560.75)
            """))
            db.execute(text("""
                INSERT INTO orders (customer_id, amount, status) VALUES 
                (1, 100.00, 'completed'), (1, 150.00, 'completed'), (1, 200.00, 'pending'),
                (2, 200.00, 'completed'), (2, 180.50, 'shipped'), (2, 510.00, 'pending'),
                (3, 340.00, 'completed'),
                (4, 500.00, 'completed'), (4, 800.00, 'completed'), (4, 800.00, 'shipped'),
                (5, 250.00, 'completed'), (5, 310.75, 'completed')
            """))
            db.commit()
        
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'products')"))
        if not result.scalar():
            db.execute(text("""
                CREATE TABLE products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200),
                    category VARCHAR(100),
                    price DECIMAL(10,2),
                    stock INTEGER,
                    rating DECIMAL(3,2)
                )
            """))
            db.execute(text("""
                INSERT INTO products (name, category, price, stock, rating) VALUES 
                ('Wireless Headphones', 'Electronics', 79.99, 150, 4.5),
                ('Smart Watch', 'Electronics', 199.99, 85, 4.7),
                ('Laptop Stand', 'Accessories', 49.99, 200, 4.3),
                ('USB-C Cable', 'Accessories', 12.99, 500, 4.6),
                ('Bluetooth Speaker', 'Electronics', 129.99, 120, 4.8),
                ('Webcam HD', 'Electronics', 89.99, 75, 4.4),
                ('Keyboard Mechanical', 'Accessories', 159.99, 60, 4.9),
                ('Mouse Wireless', 'Accessories', 39.99, 180, 4.2)
            """))
            db.commit()
        
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'employees')"))
        if not result.scalar():
            db.execute(text("""
                CREATE TABLE employees (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    department VARCHAR(100),
                    salary DECIMAL(10,2),
                    hire_date DATE,
                    manager_id INTEGER REFERENCES employees(id)
                )
            """))
            db.execute(text("""
                INSERT INTO employees (name, department, salary, hire_date, manager_id) VALUES 
                ('Sarah Johnson', 'Engineering', 120000.00, '2020-01-15', NULL),
                ('Tom Anderson', 'Engineering', 95000.00, '2021-03-10', 1),
                ('Lisa Chen', 'Engineering', 98000.00, '2021-06-20', 1),
                ('Mike Roberts', 'Sales', 85000.00, '2019-11-05', NULL),
                ('Emily Davis', 'Sales', 72000.00, '2022-02-14', 4),
                ('David Kim', 'Marketing', 78000.00, '2020-08-22', NULL),
                ('Anna Martinez', 'Marketing', 68000.00, '2022-05-30', 6)
            """))
            db.commit()
        
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'demo_posts')"))
        if not result.scalar():
            db.execute(text("""
                CREATE TABLE demo_posts (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200),
                    body TEXT,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            db.execute(text("""
                INSERT INTO demo_posts (title, body, user_id) VALUES 
                ('Getting Started with APIs', 'Learn how to work with REST APIs and make HTTP requests. This guide covers the basics of GET, POST, PUT, and DELETE methods.', 1),
                ('Database Design Best Practices', 'Explore the fundamentals of database normalization, indexing strategies, and query optimization for better performance.', 2),
                ('Modern Web Development', 'Discover the latest trends in web development including React, Vue, and modern CSS frameworks.', 3),
                ('Building Scalable Backends', 'Tips and techniques for creating robust backend systems that can handle millions of requests.', 1),
                ('Introduction to Docker', 'Containerization made easy. Learn how Docker can simplify your development and deployment workflow.', 4)
            """))
            db.commit()
    finally:
        db.close()

def check_rate_limit(key: str, limit: int, window: int) -> tuple[bool, int, int]:
    from backend.redis_client import redis_client
    
    if not redis_client.is_connected():
        return True, limit, window
    
    current = redis_client.incr(f"rate_limit:{key}")
    if current == 1:
        redis_client.expire(f"rate_limit:{key}", window)
    
    ttl = redis_client.ttl(f"rate_limit:{key}")
    remaining = max(0, limit - (current or 0))
    
    return (current or 0) <= limit, remaining, ttl if ttl > 0 else window
