"""
FastAPI application factory and configuration.
"""
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import RATE_LIMIT_POLICY
from src.middleware import add_security_headers, create_rate_limit_handler
from src.routes import create_router


def create_app() -> FastAPI:
    """
    Creates and configures the main FastAPI application instance.
    """
    app = FastAPI(
        title="ATS MatchProof",
        description="100% Free, zero-account ATS Resume & Job Matcher with Multi-AI failover and prompt injection defense.",
        version="1.0.0",
    )

    # Initialize rate limiter
    limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT_POLICY])
    app.state.limiter = limiter

    # Template renderer
    templates = Jinja2Templates(directory="templates")

    # Exception Handlers
    rate_limit_handler = create_rate_limit_handler(templates)
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    # Middleware
    app.middleware("http")(add_security_headers)

    # Routes
    router = create_router(templates, limiter)
    app.include_router(router)

    return app


# Default app instance
app = create_app()
