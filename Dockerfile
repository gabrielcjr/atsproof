# Lean Python 3.11 base image
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Nginx and curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Configure Nginx
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy application source code
COPY src/ ./src/
COPY templates/ ./templates/
COPY main.py .
COPY pytest.ini .
COPY docker/entrypoint.sh ./entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose ports 80 and 443 for Nginx
EXPOSE 80 443

# Healthcheck testing through Nginx HTTPS reverse proxy
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -k -f https://localhost/ || exit 1

# Start both Nginx and Uvicorn
ENTRYPOINT ["/app/entrypoint.sh"]
