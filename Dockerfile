# Lean Python 3.11 base image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY main.py .
COPY pytest.ini .

# Expose port 8000 for FastAPI Uvicorn
EXPOSE 8000

# Healthcheck testing through dedicated lightweight /healthz endpoint
HEALTHCHECK --interval=2m --timeout=5s --start-period=15s --retries=2 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Start Uvicorn backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers", "--forwarded-allow-ips=*"]

