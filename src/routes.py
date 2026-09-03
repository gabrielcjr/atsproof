"""
FastAPI route definitions for the ATS Matcher application.
"""

import json
import os
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter

from src.articles import get_all_articles, get_article_by_slug, get_related_articles
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
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

    def _resolve_language(
        request: Request, lang: Optional[str] = None, default_lang: Optional[str] = None
    ) -> str:
        """Helper to resolve active language preference from query param, path default, or cookie."""
        if lang:
            return "pt" if lang.lower().startswith("pt") else "en"
        if default_lang:
            return default_lang
        req_cookie = request.cookies.get("lang", "en")
        return "pt" if req_cookie.lower().startswith("pt") else "en"

    # -------------------------------------------------------------
    # Health Check & Diagnostics
    # -------------------------------------------------------------

    @router.get("/healthz")
    @router.get("/health")
    async def health_check():
        """Lightweight health check endpoint for container probes."""
        return {"status": "ok"}

    # -------------------------------------------------------------
    # Core Application Routes
    # -------------------------------------------------------------

    @router.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def index(request: Request, lang: Optional[str] = None):
        """Serves the main ATS matcher application in chosen language."""
        resolved_lang = _resolve_language(request, lang)
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
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route("/guide", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route("/guia-ats", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route(
        "/como-funciona", methods=["GET", "HEAD"], response_class=HTMLResponse
    )
    async def guide(request: Request, lang: Optional[str] = None):
        """Serves the comprehensive ATS masterclass guide."""
        path_hint = (
            "pt"
            if ("guia" in request.url.path or "como-funciona" in request.url.path)
            else "en"
        )
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)

        response = templates.TemplateResponse(
            request=request,
            name="guide.html",
            context={
                "t": t,
                "lang": resolved_lang,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route("/about", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route("/sobre", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def about(request: Request, lang: Optional[str] = None):
        """Serves the About Us & Engineering transparency page."""
        path_hint = "pt" if "sobre" in request.url.path else "en"
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)

        response = templates.TemplateResponse(
            request=request,
            name="about.html",
            context={
                "t": t,
                "lang": resolved_lang,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route("/privacy", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route(
        "/privacidade", methods=["GET", "HEAD"], response_class=HTMLResponse
    )
    async def privacy(request: Request, lang: Optional[str] = None):
        """Serves the Privacy Policy page compliant with Google AdSense and LGPD/GDPR."""
        path_hint = "pt" if "privacidade" in request.url.path else "en"
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)

        response = templates.TemplateResponse(
            request=request,
            name="privacy.html",
            context={
                "t": t,
                "lang": resolved_lang,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route("/terms", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route("/termos", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def terms(request: Request, lang: Optional[str] = None):
        """Serves the Terms of Service page."""
        path_hint = "pt" if "termos" in request.url.path else "en"
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)

        response = templates.TemplateResponse(
            request=request,
            name="terms.html",
            context={
                "t": t,
                "lang": resolved_lang,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route("/articles", methods=["GET", "HEAD"], response_class=HTMLResponse)
    @router.api_route("/artigos", methods=["GET", "HEAD"], response_class=HTMLResponse)
    async def articles_hub(request: Request, lang: Optional[str] = None):
        """Serves the Career & ATS Knowledge Hub listing page."""
        path_hint = "pt" if "artigos" in request.url.path else "en"
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)
        all_articles = get_all_articles()

        response = templates.TemplateResponse(
            request=request,
            name="articles.html",
            context={
                "t": t,
                "lang": resolved_lang,
                "articles": all_articles,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    @router.api_route(
        "/articles/{slug}", methods=["GET", "HEAD"], response_class=HTMLResponse
    )
    @router.api_route(
        "/artigos/{slug}", methods=["GET", "HEAD"], response_class=HTMLResponse
    )
    async def article_detail(request: Request, slug: str, lang: Optional[str] = None):
        """Serves an individual in-depth career/ATS article."""
        path_hint = "pt" if "artigos" in request.url.path else "en"
        resolved_lang = _resolve_language(request, lang, default_lang=path_hint)
        t = get_translations(resolved_lang)

        article = get_article_by_slug(slug)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")

        related = get_related_articles(article["id"], limit=3)

        response = templates.TemplateResponse(
            request=request,
            name="article_detail.html",
            context={
                "t": t,
                "lang": resolved_lang,
                "article": article,
                "related_articles": related,
            },
        )
        response.set_cookie(
            key="lang", value=resolved_lang, max_age=31536000, samesite="lax"
        )
        return response

    # -------------------------------------------------------------
    # Static & Verification Assets
    # -------------------------------------------------------------

    @router.get("/download-template")
    async def download_template(request: Request, lang: Optional[str] = None):
        """Allows users to download the free ATS-optimized resume template (.docx) in EN or PT."""
        resolved_lang = _resolve_language(request, lang)
        is_pt = resolved_lang == "pt"

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

    @router.api_route("/favicon.ico", methods=["GET", "HEAD"], include_in_schema=False)
    @router.api_route(
        "/static/favicon.svg", methods=["GET", "HEAD"], include_in_schema=False
    )
    async def favicon():
        """Serves the SVG favicon for browser tabs."""
        favicon_path = os.path.join(static_dir, "favicon.svg")
        return FileResponse(path=favicon_path, media_type="image/svg+xml")

    @router.api_route("/ads.txt", methods=["GET", "HEAD"], include_in_schema=False)
    async def ads_txt():
        """Serves ads.txt for Google AdSense verification."""
        ads_path = os.path.join(static_dir, "ads.txt")
        return FileResponse(path=ads_path, media_type="text/plain")

    @router.api_route("/robots.txt", methods=["GET", "HEAD"], include_in_schema=False)
    async def robots_txt():
        """Serves robots.txt for search engines and crawlers."""
        robots_path = os.path.join(static_dir, "robots.txt")
        return FileResponse(path=robots_path, media_type="text/plain")

    @router.api_route("/sitemap.xml", methods=["GET", "HEAD"], include_in_schema=False)
    async def sitemap_xml():
        """Serves sitemap.xml for search engines."""
        sitemap_path = os.path.join(static_dir, "sitemap.xml")
        return FileResponse(path=sitemap_path, media_type="application/xml")

    # -------------------------------------------------------------
    # Analysis Endpoint
    # -------------------------------------------------------------

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
        resolved_lang = _resolve_language(request, lang)
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
                    "error_message": t["error_jd_too_long"].format(
                        max_chars=MAX_TEXT_CHARS
                    ),
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
            result, provider_name = await analyze_with_fallback(
                resume_text, sanitized_jd, language=resolved_lang
            )
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
