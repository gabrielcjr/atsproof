"""
Security middleware, trusted proxy IP extraction, body size limiting, and custom exception handlers.
"""

import ipaddress

from fastapi import Request, status
from fastapi.templating import Jinja2Templates
from slowapi.errors import RateLimitExceeded

from src.config import MAX_REQUEST_BODY_BYTES, is_trusted_proxy, logger
from src.i18n import get_translations


class _PayloadTooLargeError(Exception):
    """Internal sentinel raised when streamed request body exceeds allowed size."""


def _parse_valid_ip(raw: str) -> str:
    """Returns canonical IP string if raw is a valid IPv4/IPv6 address, else empty string."""
    if not raw:
        return ""
    try:
        return str(ipaddress.ip_address(raw.strip()))
    except ValueError:
        return ""


def get_client_ip(request: Request) -> str:
    """
    Extracts the true client IP address safely.
    Only trusts X-Forwarded-For / X-Real-IP when the immediate peer IP belongs to TRUSTED_PROXY_IPS.
    Walks X-Forwarded-For from right to left and returns the first valid untrusted hop.
    """
    peer_ip = (
        request.client.host.strip() if (request.client and request.client.host) else ""
    )
    if not is_trusted_proxy(peer_ip):
        return peer_ip or "127.0.0.1"

    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        hops = [ip.strip() for ip in forwarded.split(",") if ip.strip()]
        for hop in reversed(hops):
            valid_hop = _parse_valid_ip(hop)
            if valid_hop and not is_trusted_proxy(valid_hop):
                return valid_hop

    real_ip = _parse_valid_ip(request.headers.get("X-Real-IP", ""))
    if real_ip and not is_trusted_proxy(real_ip):
        return real_ip

    return real_ip or peer_ip or "127.0.0.1"


class RequestBodyLimitMiddleware:
    """
    Pure ASGI middleware that enforces an upper bound on HTTP request body sizes
    before FastAPI/Starlette buffers or parses multipart uploads into memory.
    """

    def __init__(
        self,
        app,
        templates: Jinja2Templates,
        max_body_bytes: int = MAX_REQUEST_BODY_BYTES,
    ):
        self.app = app
        self.templates = templates
        self.max_body_bytes = max_body_bytes

    async def _send_413(self, scope, receive, send) -> None:
        request = Request(scope)
        raw_cookie = request.cookies.get("lang", "en")
        lang = "pt" if (raw_cookie or "").lower().strip().startswith("pt") else "en"
        t = get_translations(lang)
        response = self.templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context={
                "t": t,
                "lang": lang,
                "error_title": t["error_payload_too_large_title"],
                "error_message": t["error_payload_too_large_msg"].format(
                    max_kb=self.max_body_bytes // 1024
                ),
                "error_type": "validation",
            },
            status_code=413,
        )
        await response(scope, receive, send)

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or scope.get("method") not in {
            "POST",
            "PUT",
            "PATCH",
        }:
            await self.app(scope, receive, send)
            return

        for header_name, header_val in scope.get("headers", []):
            if header_name.lower() == b"content-length":
                try:
                    if int(header_val.decode("ascii").strip()) > self.max_body_bytes:
                        await self._send_413(scope, receive, send)
                        return
                except (ValueError, UnicodeDecodeError):
                    pass

        received_bytes = 0
        limit_exceeded = False
        response_started = False

        async def limited_receive():
            nonlocal received_bytes, limit_exceeded
            message = await receive()
            if message.get("type") == "http.request":
                received_bytes += len(message.get("body", b""))
                if received_bytes > self.max_body_bytes:
                    limit_exceeded = True
                    raise _PayloadTooLargeError()
            return message

        async def send_wrapper(message):
            nonlocal response_started
            if limit_exceeded:
                return
            if message.get("type") == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, limited_receive, send_wrapper)
        except _PayloadTooLargeError:
            pass

        if limit_exceeded and not response_started:
            await self._send_413(scope, receive, send)


async def add_security_headers(request: Request, call_next):
    """
    Appends strict security headers to all HTTP responses:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: SAMEORIGIN
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: restricts camera, microphone, geolocation
    - Strict-Transport-Security: enforces HTTPS
    - Content-Security-Policy: restricts asset sources without unsafe-eval
    """
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com https://pagead2.googlesyndication.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'self';"
    )
    return response


def create_rate_limit_handler(templates: Jinja2Templates):
    """
    Returns an exception handler for RateLimitExceeded that renders a clean HTMX partial.
    """

    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        raw_cookie = request.cookies.get("lang", "en")
        lang = "pt" if (raw_cookie or "").lower().strip().startswith("pt") else "en"
        t = get_translations(lang)
        logger.warning(f"Rate limit exceeded for client: {get_client_ip(request)}")
        return templates.TemplateResponse(
            request=request,
            name="partials/rate_limit.html",
            context={"retry_after": exc.detail, "t": t, "lang": lang},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    return custom_rate_limit_handler
