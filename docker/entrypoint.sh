#!/bin/bash
set -e

echo "==> Starting Nginx reverse proxy on port 80..."
nginx

# Trap signals for graceful container shutdown
trap 'echo "==> Shutting down..."; nginx -s stop; exit 0' SIGTERM SIGINT

echo "==> Starting FastAPI Uvicorn backend on 127.0.0.1:8000..."
exec uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2 --proxy-headers --forwarded-allow-ips='*'
