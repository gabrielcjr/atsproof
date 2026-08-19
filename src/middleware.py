"""
Security middleware and custom exception handlers.
"""
from fastapi import Request, status
from fastapi.templating import Jinja2Templates
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.config import logger
from src.i18n import get_translations


async def add_security_headers(request: Request, call_next):
    """
    Appends strict security headers to all HTTP responses:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: SAMEORIGIN
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: restricts camera, microphone, geolocation
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


def create_rate_limit_handler(templates: Jinja2Templates):
    """
    Returns an exception handler for RateLimitExceeded that renders a clean HTMX partial.
    """
    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        lang = request.cookies.get("lang", "en")
        t = get_translations(lang)
        logger.warning(f"Rate limit exceeded for client: {get_remote_address(request)}")
        return templates.TemplateResponse(
            request=request,
            name="partials/rate_limit.html",
            context={"retry_after": exc.detail, "t": t, "lang": lang},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )
    return custom_rate_limit_handler
