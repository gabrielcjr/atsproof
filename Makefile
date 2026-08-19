# ==============================================================================
# ATS MatchProof — Automation Makefile
# ==============================================================================

SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTEST := $(VENV)/bin/pytest

APP_NAME := ats_matcher
DOCKER_IMAGE := ats-matcher:latest
PORT ?= 8001

.PHONY: help install dev start prod test test-unit clean stop docker-build docker-run docker-stop compose-up compose-down compose-logs

# Default target: display colorized help
help:
	@echo ""
	@echo "  \033[1;36mATS MatchProof — Available Make Commands\033[0m"
	@echo "  \033[0;34m==========================================\033[0m"
	@echo ""
	@echo "  \033[1;32mLocal Development:\033[0m"
	@echo "    \033[1;33mmake install\033[0m       Create virtualenv & install dependencies"
	@echo "    \033[1;33mmake dev\033[0m           Start local dev server with auto-reload (port $(PORT))"
	@echo "    \033[1;33mmake stop\033[0m          Stop all running local uvicorn processes"
	@echo ""
	@echo "  \033[1;32mTesting & Quality:\033[0m"
	@echo "    \033[1;33mmake test\033[0m          Run test suite using pytest"
	@echo "    \033[1;33mmake test-unit\033[0m     Run tests using standard Python unittest runner"
	@echo "    \033[1;33mmake clean\033[0m         Remove cache, pyc, and temp files"
	@echo ""
	@echo "  \033[1;32mProduction & Docker Compose (Port 80 with Nginx):\033[0m"
	@echo "    \033[1;33mmake compose-up\033[0m    Build & start production container (Nginx + FastAPI) on port 80"
	@echo "    \033[1;33mmake compose-down\033[0m  Stop and remove compose deployment"
	@echo "    \033[1;33mmake compose-logs\033[0m  Follow live production container logs"
	@echo "    \033[1;33mmake docker-build\033[0m  Build standalone Docker image"
	@echo "    \033[1;33mmake docker-run\033[0m    Run standalone container on port 80"
	@echo "    \033[1;33mmake docker-stop\033[0m   Stop running Docker container"
	@echo ""

# Setup environment
install:
	@echo "==> Creating virtual environment..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "==> Installing project dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@test -f .env || cp .env.example .env
	@echo "==> Setup complete! Update .env with your API keys if needed."

# Run local development server
dev:
	@echo "==> Starting ATS MatchProof dev server on http://127.0.0.1:$(PORT)..."
	@$(UVICORN) main:app --host 127.0.0.1 --port $(PORT) --reload

# Run local production server
prod:
	@echo "==> Starting ATS MatchProof in production mode (2 workers) on port 8000..."
	@$(UVICORN) main:app --host 0.0.0.0 --port 8000 --workers 2

start: prod

# Run test suite
test:
	@echo "==> Running pytest test suite..."
	@$(PYTEST) -v

test-unit:
	@echo "==> Running unit tests via unittest runner..."
	@$(PYTHON) -m unittest discover -s src/test -p "test_*.py" -v

# Clean caches and temporary artifacts
clean:
	@echo "==> Cleaning cache and temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name "*.pyd" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .coverage htmlcov .ruff_cache 2>/dev/null || true
	@echo "==> Cleaned up successfully."

# Stop running uvicorn servers
stop:
	@echo "==> Stopping running uvicorn instances..."
	@-pkill -f "uvicorn main:app" 2>/dev/null || true
	@echo "==> Stopped."

# Docker Compose targets (Single-container Nginx + FastAPI on Port 80)
compose-up:
	@echo "==> Deploying ATS MatchProof with Docker Compose on port 80..."
	@docker compose up -d --build
	@echo "==> Deployment ready on http://localhost (Port 80)!"

compose-down:
	@echo "==> Stopping Docker Compose deployment..."
	@docker compose down
	@echo "==> Deployment stopped."

compose-logs:
	@docker compose logs -f

# Standalone Docker targets
docker-build:
	@echo "==> Building Docker image: $(DOCKER_IMAGE)..."
	@docker build -t $(DOCKER_IMAGE) .

docker-run:
	@echo "==> Running $(DOCKER_IMAGE) with Nginx on http://127.0.0.1:80..."
	@docker run --rm -d --name $(APP_NAME) -p 80:80 --env-file .env $(DOCKER_IMAGE)
	@echo "==> Container started! View logs with: docker logs -f $(APP_NAME)"

docker-stop:
	@echo "==> Stopping Docker container $(APP_NAME)..."
	@-docker stop $(APP_NAME) 2>/dev/null || true
	@echo "==> Container stopped."
