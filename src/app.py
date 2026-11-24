import os

import logfire
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded

from src.config import (
    MAX_REQUEST_BODY_BYTES,
    RATE_LIMIT_POLICY,
    RATE_LIMIT_STORAGE_URI,
)
from src.middleware import (
    RequestBodyLimitMiddleware,
    add_security_headers,
    create_rate_limit_handler,
    get_client_ip,
)
from src.routes import create_router

# Configure Pydantic Logfire for observability
logfire_token = os.getenv("LOGFIRE_TOKEN", "").strip()
if logfire_token:
    logfire.configure(token=logfire_token, send_to_logfire=True)
else:
    logfire.configure(send_to_logfire=False)


def create_app() -> FastAPI:
    """
    Creates and configures the main FastAPI application instance.
    """
    app = FastAPI(
        title="ATS MatchProof",
        description="100% Free, zero-account ATS Resume & Job Matcher with Multi-AI failover and prompt injection defense.",
        version="1.0.0",
    )

    # Instrument FastAPI & Pydantic models with Logfire (excluding health checks to avoid log noise)
    logfire.instrument_fastapi(app, excluded_urls="healthz,health,favicon.ico")
    logfire.instrument_pydantic()

    # OpenTelemetry Tracing to Tempo (if configured)
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if otel_endpoint:
        try:
            from opentelemetry import trace
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter,
            )
            from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            target_endpoint = (
                otel_endpoint
                if otel_endpoint.endswith("/v1/traces")
                else f"{otel_endpoint}/v1/traces"
            )
            provider = trace.get_tracer_provider()
            if hasattr(provider, "add_span_processor"):
                provider.add_span_processor(
                    BatchSpanProcessor(OTLPSpanExporter(endpoint=target_endpoint))
                )
            HTTPXClientInstrumentor().instrument()
        except Exception as e:
            print(f"Failed to initialize OpenTelemetry for ATS MatchProof: {e}")

    # Initialize rate limiter keyed by true client IP
    limiter = Limiter(
        key_func=get_client_ip,
        default_limits=[RATE_LIMIT_POLICY],
        storage_uri=RATE_LIMIT_STORAGE_URI,
    )
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

    # Middleware (RequestBodyLimitMiddleware registered first so add_security_headers wraps 413 too)
    app.add_middleware(
        RequestBodyLimitMiddleware,
        templates=templates,
        max_body_bytes=MAX_REQUEST_BODY_BYTES,
    )
    app.middleware("http")(add_security_headers)

    # Routes
    router = create_router(templates, limiter)
    app.include_router(router)

    return app


# Default app instance
app = create_app()
