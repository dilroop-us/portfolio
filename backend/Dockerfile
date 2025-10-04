FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install uv and dependencies
RUN pip install uv && \
    uv pip install --system -r pyproject.toml

# Copy application code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run with multiple workers for production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]