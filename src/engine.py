import asyncio
import json
import math
import re
import unicodedata
from typing import Dict, List, Optional, Set, Tuple

import logfire

from src.config import (
    LLM_CALL_TIMEOUT_SECONDS,
    MAX_CONCURRENT_REQUESTS,
    SEMAPHORE_TIMEOUT_SECONDS,
    get_gemini_api_key,
    get_groq_api_key,
    logger,
)
from src.prompts import (
    JSON_SCHEMA_DESCRIPTION,
    SYSTEM_INSTRUCTION,
    build_user_prompt,
)
from src.schemas import ATSMatchResult

STOP_WORDS: Set[str] = {
    "and",
    "the",
    "or",
    "in",
    "on",
    "at",
    "to",
    "for",
    "with",
    "by",
    "of",
    "a",
    "an",
    "e",
    "o",
    "os",
    "as",
    "em",
    "de",
    "do",
    "da",
    "dos",
    "das",
    "para",
    "com",
    "por",
}


def _strip_accents(s: str) -> str:
    """Normalizes Unicode text by stripping combining diacritical marks (e.g. gestão -> gestao)."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _has_token_boundary(token: str, text: str) -> bool:
    """Checks if token appears in text bounded by non-word characters (supporting symbols like C++, .NET, Node.js)."""
    if not token:
        return False
    escaped = re.escape(token)
    return bool(re.search(r"(?<![a-zA-Z0-9_])" + escaped + r"(?![a-zA-Z0-9_])", text))


def is_keyword_in_text(keyword: str, text: str) -> bool:
    """
    Generalized lexical & token presence matcher (zero hardcoded dictionaries).
    Validates whether a keyword, acronym, or its component tokens exist in the text.
    Works universally across tech, business, medical, and multi-lingual (EN/PT) domains.
    """
    if not keyword or not text:
        return False

    kw_raw = keyword.strip()
    kw_norm = _strip_accents(kw_raw).lower()
    text_norm = _strip_accents(text).lower()

    # 1. Direct whole phrase with strict token boundary check (prevents 'Java' matching 'JavaScript' or 'Go' matching 'good')
    if _has_token_boundary(kw_norm, text_norm):
        return True

    # 2. Punctuation-stripped token match (e.g. Node.js <-> nodejs, Nest.js <-> NestJS, CI/CD <-> cicd)
    kw_clean = re.sub(r"[^a-z0-9]", "", kw_norm)
    text_tokens_clean = {
        re.sub(r"[^a-z0-9]", "", tok)
        for tok in re.split(r"[\s,;()\[\]{}\"'|]+", text_norm)
        if tok
    }
    # Also collapse slash/hyphen/dot separated pairs in text (e.g. "ci/cd" -> "cicd", "node.js" -> "nodejs")
    for compound in re.findall(r"[a-z0-9]+(?:[./\-][a-z0-9]+)+", text_norm):
        text_tokens_clean.add(re.sub(r"[^a-z0-9]", "", compound))

    if kw_clean and len(kw_clean) >= 3 and kw_clean in text_tokens_clean:
        return True

    # 3. Acronym search (e.g. capitalized acronyms like DDD, GA4, AWS, GCP, SQS, NGS, CI/CD)
    raw_without_parens = _strip_accents(kw_raw)
    acronym_match = re.findall(r"\b[A-Z0-9]{2,}\b", raw_without_parens)
    for acr in acronym_match:
        if _has_token_boundary(acr.lower(), text_norm):
            return True

    # 4. Multi-word phrase component check (e.g. "Domain-Driven Design (DDD)", "AWS EC2", "HubSpot CRM")
    # Strip parenthetical acronym suffixes if present so we can check core phrase or individual components
    parts = [
        re.sub(r"[^a-z0-9]", "", p) for p in re.split(r"[\s/(),_\-]+", kw_norm) if p
    ]
    meaningful_parts = [p for p in parts if p not in STOP_WORDS and len(p) >= 2]

    if not meaningful_parts:
        return False

    matched_parts = 0
    for part in meaningful_parts:
        if _has_token_boundary(part, text_norm) or (
            len(part) >= 3 and part in text_tokens_clean
        ):
            matched_parts += 1
        elif (
            len(part) >= 5
            and part.endswith("s")
            and _has_token_boundary(part[:-1], text_norm)
        ):
            matched_parts += 1

    if len(meaningful_parts) == 1:
        return matched_parts == 1

    # Require majority of meaningful tokens (or first primary head token for 2-word vendor/cloud pairs like "AWS EC2")
    required_matches = math.ceil(len(meaningful_parts) * 0.6)
    if matched_parts >= required_matches:
        return True

    # Special case for 2-token compound where first token is a specific proper technical identifier (e.g. "AWS EC2" matching "AWS")
    if (
        len(meaningful_parts) == 2
        and len(meaningful_parts[0]) >= 3
        and _has_token_boundary(meaningful_parts[0], text_norm)
        and meaningful_parts[0] in {a.lower() for a in acronym_match}
    ):
        return True

    return False


def sanitize_and_align_keywords(
    result: ATSMatchResult, resume_text: str, job_desc: str
) -> ATSMatchResult:
    """
    Generalized alignment layer:
    - matched_keywords: must have evidence in both Job Description AND Resume.
    - missing_critical_keywords: must have evidence in Job Description AND NOT in Resume.
    - Eliminates any fabricated, hallucinated, or unrequested resume skills from matched_keywords.
    """
    clean_matched: List[str] = []
    seen_matched: Set[str] = set()

    for kw in result.matched_keywords or []:
        normalized = kw.strip()
        norm_lower = _strip_accents(normalized).lower()
        if not normalized or norm_lower in seen_matched:
            continue

        # Must have lexical or token presence in both Job Description AND Resume
        if is_keyword_in_text(normalized, job_desc) and is_keyword_in_text(
            normalized, resume_text
        ):
            seen_matched.add(norm_lower)
            clean_matched.append(normalized)

    result.matched_keywords = clean_matched

    clean_missing: List[str] = []
    seen_missing: Set[str] = set()

    for kw in result.missing_critical_keywords or []:
        normalized = kw.strip()
        norm_lower = _strip_accents(normalized).lower()
        if not normalized or norm_lower in seen_missing or norm_lower in seen_matched:
            continue

        # Must have lexical presence in Job Description and NOT in Resume
        if is_keyword_in_text(normalized, job_desc) and not is_keyword_in_text(
            normalized, resume_text
        ):
            seen_missing.add(norm_lower)
            clean_missing.append(normalized)

    result.missing_critical_keywords = clean_missing

    return result


# Concurrency semaphore to throttle active LLM calls
concurrency_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Cached SDK clients keyed by API key
_gemini_clients: Dict[str, object] = {}
_groq_clients: Dict[str, object] = {}


def _get_gemini_client(api_key: str):
    from google import genai

    client = _gemini_clients.get(api_key)
    if client is None:
        client = genai.Client(api_key=api_key)
        _gemini_clients[api_key] = client
    return client


def _get_groq_client(api_key: str):
    from groq import AsyncGroq

    client = _groq_clients.get(api_key)
    if client is None:
        client = AsyncGroq(api_key=api_key)
        _groq_clients[api_key] = client
    return client


async def call_gemini_primary(
    resume_text: str, job_desc: str, language: str = "en"
) -> ATSMatchResult:
    """
    Primary Engine: Google GenAI using official async SDK and native JSON schema output.
    """
    api_key = get_gemini_api_key()
    from google.genai import types

    client = _get_gemini_client(api_key)
    prompt_content = build_user_prompt(resume_text, job_desc, language=language)

    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
    ]
    last_err: Optional[Exception] = None

    with logfire.span("Gemini Primary Engine", language=language):
        for model_name in candidate_models:
            try:
                with logfire.span("Gemini Call", model=model_name):
                    gen_config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=ATSMatchResult,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=True
                        ),
                        temperature=0.2,
                    )
                    response = await asyncio.wait_for(
                        client.aio.models.generate_content(
                            model=model_name,
                            contents=prompt_content,
                            config=gen_config,
                        ),
                        timeout=LLM_CALL_TIMEOUT_SECONDS,
                    )
                    if response and response.text:
                        data = json.loads(response.text)
                        logfire.info("Gemini analysis succeeded", model=model_name)
                        return ATSMatchResult.model_validate(data)
            except Exception as e:
                last_err = e
                logfire.warn(
                    "Gemini model candidate failed", model=model_name, error=str(e)
                )
                logger.warning(
                    f"Gemini model {model_name} failed: {e}. Trying next candidate..."
                )

    raise last_err or ValueError("Failed to obtain response from Gemini flash models.")


async def call_groq_fallback(
    resume_text: str, job_desc: str, language: str = "en"
) -> Tuple[ATSMatchResult, str]:
    """
    Fallback Engine: Groq Free Tier open-weight models using AsyncGroq and JSON object mode.
    """
    api_key = get_groq_api_key()
    client = _get_groq_client(api_key)

    system_content = f"{SYSTEM_INSTRUCTION}\n\nRespond strictly with a single valid JSON object matching this schema:\n{JSON_SCHEMA_DESCRIPTION}"
    prompt_content = build_user_prompt(resume_text, job_desc, language=language)

    candidate_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    ]
    last_err: Optional[Exception] = None

    with logfire.span("Groq Failover Engine", language=language):
        for model_name in candidate_models:
            try:
                with logfire.span("Groq Call", model=model_name):
                    response = await asyncio.wait_for(
                        client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": system_content},
                                {"role": "user", "content": prompt_content},
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.2,
                        ),
                        timeout=LLM_CALL_TIMEOUT_SECONDS,
                    )
                    raw_content = response.choices[0].message.content
                    if raw_content:
                        clean_text = raw_content.strip()
                        # Strip reasoning/thinking tags if returned by reasoning models
                        if "</think>" in clean_text:
                            clean_text = clean_text.split("</think>")[-1].strip()
                        if clean_text.startswith("```json"):
                            clean_text = clean_text[7:]
                        if clean_text.startswith("```"):
                            clean_text = clean_text[3:]
                        if clean_text.endswith("```"):
                            clean_text = clean_text[:-3]
                        data = json.loads(clean_text.strip())
                        logfire.info(
                            "Groq failover analysis succeeded", model=model_name
                        )
                        return (
                            ATSMatchResult.model_validate(data),
                            f"ATS DeepScan Engine ({model_name})",
                        )
            except Exception as e:
                last_err = e
                logfire.warn(
                    "Groq model candidate failed", model=model_name, error=str(e)
                )
                logger.warning(
                    f"Groq model {model_name} failed: {e}. Trying next open model..."
                )

    raise last_err or ValueError("Failed to obtain response from Groq models.")


async def analyze_with_fallback(
    resume_text: str, job_desc: str, language: str = "en"
) -> Tuple[ATSMatchResult, str]:
    """
    Coordinates primary Gemini call with automatic failover to Groq.
    Enforces bounded concurrency wait + per-call timeouts, validates keyword presence
    against the JD, and returns (ATSMatchResult, white_label_engine_name).
    """
    try:
        await asyncio.wait_for(
            concurrency_semaphore.acquire(), timeout=SEMAPHORE_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        logger.warning("Concurrency semaphore acquisition timed out.")
        raise RuntimeError(
            "ATS verification services are experiencing high concurrency. Please try again shortly."
        )

    try:
        with logfire.span("Dual Engine Match Analysis", language=language):
            # 1. Attempt Primary Engine (Google Gemini)
            try:
                logger.info("Dispatching analysis to primary engine...")
                result = await call_gemini_primary(
                    resume_text, job_desc, language=language
                )
                result = sanitize_and_align_keywords(result, resume_text, job_desc)
                return result, "ATS DeepScan Engine • Active"
            except Exception as e:
                logger.warning(
                    f"Primary engine call failed: {e}. Routing to failover engine..."
                )
                logfire.warn("Primary engine failed, triggering failover", error=str(e))

            # 2. Attempt Secondary Failover Engine (Groq Open-Weight)
            try:
                logger.info("Dispatching analysis to secondary failover engine...")
                result, _ = await call_groq_fallback(
                    resume_text, job_desc, language=language
                )
                result = sanitize_and_align_keywords(result, resume_text, job_desc)
                return result, "ATS DeepScan Engine (Failover Mode)"
            except Exception as groq_e:
                logger.error(f"Secondary failover engine call also failed: {groq_e}")
                logfire.error(
                    "Secondary failover engine also failed", error=str(groq_e)
                )
                raise RuntimeError(
                    "ATS verification services temporarily unavailable. Please try again shortly."
                )
    finally:
        concurrency_semaphore.release()
