# Lean Python 3.11 base image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthchecks and create unprivileged runtime user
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser

# Copy and install runtime python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code with non-root ownership
COPY --chown=10001:10001 src/ ./src/
COPY --chown=10001:10001 templates/ ./templates/
COPY --chown=10001:10001 static/ ./static/
COPY --chown=10001:10001 main.py .

# Drop privileges
USER 10001:10001

# Expose port 8000 for FastAPI Uvicorn
EXPOSE 8000

# Healthcheck testing through dedicated lightweight /healthz endpoint
HEALTHCHECK --interval=2m --timeout=5s --start-period=15s --retries=2 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Start single-worker Uvicorn backend so in-memory rate limits & semaphore are exact per pod
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers", "--forwarded-allow-ips=127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"]
