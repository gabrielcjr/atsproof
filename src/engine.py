import asyncio
import json
import re
from typing import List, Set, Tuple

import logfire

from src.config import (
    MAX_CONCURRENT_REQUESTS,
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
    "a",
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


def is_keyword_in_text(keyword: str, text: str) -> bool:
    """
    Generalized lexical & token presence matcher (zero hardcoded dictionaries).
    Validates whether a keyword, acronym, or its component tokens exist in the text.
    Works universally across tech, business, medical, and multi-lingual domains.
    """
    if not keyword or not text:
        return False

    kw_raw = keyword.strip()
    kw_lower = kw_raw.lower()
    text_lower = text.lower()

    # 1. Direct whole phrase or regex word boundary check
    escaped_kw = re.escape(kw_lower)
    if (
        re.search(r"(?:\b|_)" + escaped_kw + r"(?:\b|_)", text_lower)
        or kw_lower in text_lower
    ):
        return True

    # 2. Punctuation stripped check (e.g. Node.js -> nodejs, Nest.js -> nestjs, CI/CD -> cicd)
    kw_clean = re.sub(r"[^a-zA-Z0-9]", "", kw_lower)
    text_clean = re.sub(r"[^a-zA-Z0-9]", "", text_lower)
    if kw_clean and len(kw_clean) >= 3 and kw_clean in text_clean:
        return True

    # 3. Acronym search (e.g. capitalized acronyms like DDD, GA4, AWS, GCP, SQS, CI/CD)
    acronym_match = re.findall(r"\b[A-Z0-9]{2,}\b", kw_raw)
    for acr in acronym_match:
        if re.search(r"\b" + re.escape(acr.lower()) + r"\b", text_lower):
            return True

    # 4. Multi-word phrase component check (e.g. "Domain-Driven Design (DDD)", "AWS EC2", "RESTful APIs")
    parts = [
        re.sub(r"[^a-zA-Z0-9]", "", p).lower()
        for p in re.split(r"[\s/(),_\-]+", kw_raw)
        if len(p) >= 2
    ]
    meaningful_parts = [p for p in parts if p not in STOP_WORDS and len(p) >= 2]

    for part in meaningful_parts:
        if len(part) <= 2:
            if re.search(r"\b" + re.escape(part) + r"\b", text_lower):
                return True
        else:
            if part in text_lower or (len(part) >= 3 and part in text_clean):
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
        norm_lower = normalized.lower()
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
        norm_lower = normalized.lower()
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


async def call_gemini_primary(
    resume_text: str, job_desc: str, language: str = "en"
) -> ATSMatchResult:
    """
    Primary Engine: Google GenAI using official SDK and native JSON schema output.
    """
    api_key = get_gemini_api_key()

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    prompt_content = build_user_prompt(resume_text, job_desc, language=language)

    candidate_models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.0-flash",
    ]
    last_err = None

    with logfire.span("Gemini Primary Engine", language=language):
        for model_name in candidate_models:
            try:
                with logfire.span("Gemini Call", model=model_name):

                    def _run_gemini(m=model_name):
                        return client.models.generate_content(
                            model=m,
                            contents=prompt_content,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                response_mime_type="application/json",
                                response_schema=ATSMatchResult,
                                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                                    disable=True
                                ),
                                temperature=0.2,
                            ),
                        )

                    response = await asyncio.to_thread(_run_gemini)
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
    Fallback Engine: Groq Free Tier open-weight models using JSON object mode.
    """
    api_key = get_groq_api_key()

    from groq import Groq

    client = Groq(api_key=api_key)

    system_content = f"{SYSTEM_INSTRUCTION}\n\nRespond strictly with a single valid JSON object matching this schema:\n{JSON_SCHEMA_DESCRIPTION}"
    prompt_content = build_user_prompt(resume_text, job_desc, language=language)

    candidate_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
    ]
    last_err = None

    with logfire.span("Groq Failover Engine", language=language):
        for model_name in candidate_models:
            try:
                with logfire.span("Groq Call", model=model_name):

                    def _run_groq(m=model_name):
                        return client.chat.completions.create(
                            model=m,
                            messages=[
                                {"role": "system", "content": system_content},
                                {"role": "user", "content": prompt_content},
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.2,
                        )

                    response = await asyncio.to_thread(_run_groq)
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
    Enforces concurrency limits, validates keyword presence against the JD,
    and returns (ATSMatchResult, white_label_engine_name).
    """
    async with concurrency_semaphore:
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
