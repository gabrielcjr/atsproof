"""
FastAPI route definitions for the ATS Matcher application.
"""
import json
import os
from typing import Optional
from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter

from src.config import (
    MAX_PDF_PAGES,
    MAX_PDF_SIZE_BYTES,
    MAX_TEXT_CHARS,
    RATE_LIMIT_POLICY,
    logger,
)
from src.engine import analyze_with_fallback
from src.extractor import extract_text_from_pdf_bytes
from src.i18n import get_translations


def create_router(templates: Jinja2Templates, limiter: Limiter) -> APIRouter:
    """
    Router factory configured with template rendering and rate limiting.
    """
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request, lang: Optional[str] = None):
        """Serves the main ATS matcher single page application in chosen language."""
        req_lang = lang or request.cookies.get("lang", "en")
        resolved_lang = "pt" if req_lang.lower().startswith("pt") else "en"
        t = get_translations(resolved_lang)

        response = templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "t": t,
                "lang": resolved_lang,
                "max_pdf_kb": MAX_PDF_SIZE_BYTES // 1024,
                "max_pages": MAX_PDF_PAGES,
                "max_chars": MAX_TEXT_CHARS,
            },
        )
        response.set_cookie(key="lang", value=resolved_lang, max_age=31536000, samesite="lax")
        return response

    @router.get("/download-template")
    async def download_template(request: Request, lang: Optional[str] = None):
        """Allows users to download the free ATS-optimized resume template (.docx) in EN or PT."""
        req_lang = lang or request.cookies.get("lang", "en")
        is_pt = req_lang.lower().startswith("pt")

        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
        if is_pt:
            template_path = os.path.join(static_dir, "resume_template_pt.docx")
            filename = "Modelo_Curriculo_ATS.docx"
        else:
            template_path = os.path.join(static_dir, "resume_template.docx")
            filename = "ATS_Resume_Template.docx"

        if not os.path.exists(template_path):
            template_path = os.path.join(static_dir, "resume_template.docx")

        return FileResponse(
            path=template_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    @router.get("/favicon.ico", include_in_schema=False)
    @router.get("/static/favicon.svg", include_in_schema=False)
    async def favicon():
        """Serves the SVG favicon for browser tabs."""
        favicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "favicon.svg")
        if not os.path.exists(favicon_path):
            favicon_path = "static/favicon.svg"
        return FileResponse(path=favicon_path, media_type="image/svg+xml")

    @router.get("/ads.txt", include_in_schema=False)
    async def ads_txt():
        """Serves ads.txt for Google AdSense verification."""
        ads_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "ads.txt")
        if not os.path.exists(ads_path):
            ads_path = "static/ads.txt"
        return FileResponse(path=ads_path, media_type="text/plain")

    @router.post("/analyze", response_class=HTMLResponse)
    @limiter.limit(RATE_LIMIT_POLICY)
    async def analyze_match(
        request: Request,
        resume: UploadFile = File(...),
        job_description: str = Form(...),
        honeypot: Optional[str] = Form(None),
        lang: Optional[str] = Form(None),
    ):
        """
        Analyzes uploaded resume against job description.
        Enforces honeypot check, in-memory PDF extraction, dual-LLM fallback, and i18n.
        """
        req_lang = lang or request.cookies.get("lang", "en")
        resolved_lang = "pt" if req_lang.lower().startswith("pt") else "en"
        t = get_translations(resolved_lang)

        # 1. Anti-bot honeypot check
        if honeypot and honeypot.strip():
            logger.warning("Bot honeypot triggered on /analyze submission.")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["error_default_title"],
                    "error_message": t["error_bot_msg"],
                    "error_type": "client",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Validate Job Description text
        sanitized_jd = (job_description or "").strip()
        if not sanitized_jd:
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["jd_col_title"],
                    "error_message": t["error_jd_empty"],
                    "error_type": "validation",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if len(sanitized_jd) > MAX_TEXT_CHARS:
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["jd_col_title"],
                    "error_message": t["error_jd_too_long"].format(max_chars=MAX_TEXT_CHARS),
                    "error_type": "validation",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Read & Validate Uploaded Resume PDF (strictly in-memory)
        try:
            pdf_bytes = await resume.read()
            if not pdf_bytes:
                return templates.TemplateResponse(
                    request=request,
                    name="partials/error.html",
                    context={
                        "t": t,
                        "lang": resolved_lang,
                        "error_title": t["upload_col_title"],
                        "error_message": t["error_pdf_empty"],
                        "error_type": "validation",
                    },
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            resume_text = extract_text_from_pdf_bytes(pdf_bytes)
        except ValueError as ve:
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["upload_col_title"],
                    "error_message": str(ve),
                    "error_type": "validation",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected file reading error: {e}")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["upload_col_title"],
                    "error_message": t["error_pdf_read"],
                    "error_type": "validation",
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 4. Run AI Analysis with Fallback & Language Target
        try:
            result, provider_name = await analyze_with_fallback(resume_text, sanitized_jd, language=resolved_lang)
            result_payload = result.model_dump()
            result_payload["provider"] = provider_name
            return templates.TemplateResponse(
                request=request,
                name="partials/results.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "result": result,
                    "result_json": json.dumps(result_payload),
                    "provider": provider_name,
                },
            )
        except Exception as e:
            logger.error(f"Analysis engine failure: {e}")
            return templates.TemplateResponse(
                request=request,
                name="partials/error.html",
                context={
                    "t": t,
                    "lang": resolved_lang,
                    "error_title": t["error_high_demand_title"],
                    "error_message": t["error_high_demand_msg"],
                    "error_type": "server",
                    "suggestion": t["error_suggestion_retry"],
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return router
