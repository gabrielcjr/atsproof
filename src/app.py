import os
import logfire
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import RATE_LIMIT_POLICY
from src.middleware import add_security_headers, create_rate_limit_handler
from src.routes import create_router

# Configure Pydantic Logfire for observability
logfire_token = os.getenv("LOGFIRE_TOKEN", "").strip()
if logfire_token:
    logfire.configure(token=logfire_token, send_to_logfire=True)
else:
    logfire.configure(send_to_logfire=False)


def get_client_ip(request) -> str:
    """Extracts the true client IP address behind reverse proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


def create_app() -> FastAPI:
    """
    Creates and configures the main FastAPI application instance.
    """
    app = FastAPI(
        title="ATS MatchProof",
        description="100% Free, zero-account ATS Resume & Job Matcher with Multi-AI failover and prompt injection defense.",
        version="1.0.0",
    )

    # Instrument FastAPI & Pydantic models with Logfire
    logfire.instrument_fastapi(app)
    logfire.instrument_pydantic()

    # Initialize rate limiter keyed by true client IP
    limiter = Limiter(key_func=get_client_ip, default_limits=[RATE_LIMIT_POLICY])
    app.state.limiter = limiter

    # Template renderer
    templates = Jinja2Templates(directory="templates")

    # Static Assets (CSS, JS, Favicon, Docx Templates)
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    if not os.path.exists(static_dir):
        static_dir = "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
