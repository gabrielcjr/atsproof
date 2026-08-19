"""
FastAPI route definitions for the ATS Matcher application.
"""
from typing import Optional
from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.config import (
    MAX_PDF_PAGES,
    MAX_PDF_SIZE_BYTES,
    MAX_TEXT_CHARS,
    RATE_LIMIT_POLICY,
    logger,
)
from src.engine import analyze_with_fallback
from src.extractor import extract_text_from_pdf_bytes


def create_router(templates: Jinja2Templates, limiter: Limiter) -> APIRouter:
    """
    Router factory configured with template rendering and rate limiting.
    """
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Serves the main ATS matcher single page application."""
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "max_pdf_kb": MAX_PDF_SIZE_BYTES // 1024,
                "max_pages": MAX_PDF_PAGES,
                "max_chars": MAX_TEXT_CHARS,
            },
        )

    @router.post("/analyze", response_class=HTMLResponse)
    @limiter.limit(RATE_LIMIT_POLICY)
    async def analyze_match(
        request: Request,
        resume: UploadFile = File(...),
        job_description: str = Form(...),
        honeypot: Optional[str] = Form(None),
    ):
        """
        Analyzes uploaded resume against job description.
        Enforces honeypot check, in-memory PDF extraction, and dual-LLM fallback.
        """
        # 1. Honeypot check (anti-bot trap)
        if honeypot and honeypot.strip():
            logger.warning(f"Bot detected via honeypot trap from {get_remote_address(request)}")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={"error_message": "Automated submission rejected."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Validate Job Description text
        sanitized_jd = (job_description or "").strip()
        if not sanitized_jd:
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={"error_message": "Job Description cannot be empty. Please paste the job listing text."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if len(sanitized_jd) > MAX_TEXT_CHARS:
            sanitized_jd = sanitized_jd[:MAX_TEXT_CHARS]

        # 3. Read & Validate Uploaded Resume PDF (strictly in-memory)
        try:
            pdf_bytes = await resume.read()
            if not pdf_bytes:
                return templates.TemplateResponse(
                    request=request,
                    name="partials/error.html",
                    context={"error_message": "Uploaded resume file is empty."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            resume_text = extract_text_from_pdf_bytes(pdf_bytes)
        except ValueError as ve:
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={"error_message": str(ve)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected file reading error: {e}")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={"error_message": "Failed to read the uploaded resume file. Please ensure it is a valid PDF."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Run AI Analysis with Fallback
        try:
            result, provider_name = await analyze_with_fallback(resume_text, sanitized_jd)
            return templates.TemplateResponse(
                request=request,
                name="partials/results.html",
                context={
                    "result": result,
                    "provider": provider_name,
                },
            )
        except Exception as e:
            logger.error(f"Analysis engine failure: {e}")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "error_message": f"AI ATS Engine temporarily unavailable: {str(e)}. Please check your API keys or try again shortly."
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return router
