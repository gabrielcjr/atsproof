"""
Dual-Engine AI Dispatcher with multi-key failover and concurrency limits.
Primary: Google GenAI (Gemini 3.6 Flash / 2.5 Flash Lite)
Failover: Groq (LLaMA 3.3 70B / LLaMA 3.1 8B)
"""
import asyncio
import json
from typing import Tuple

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

# Concurrency semaphore to throttle active LLM calls
concurrency_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def call_gemini_primary(resume_text: str, job_desc: str) -> ATSMatchResult:
    """
    Primary Engine: Google GenAI using official SDK and native JSON schema output.
    """
    api_key = get_gemini_api_key()

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    prompt_content = build_user_prompt(resume_text, job_desc)

    candidate_models = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]
    last_err = None

    with logfire.span("Gemini Primary Engine"):
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
                                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                                temperature=0.2,
                            )
                        )

                    response = await asyncio.to_thread(_run_gemini)
                    if response and response.text:
                        data = json.loads(response.text)
                        logfire.info("Gemini analysis succeeded", model=model_name)
                        return ATSMatchResult.model_validate(data)
            except Exception as e:
                last_err = e
                logfire.warn("Gemini model candidate failed", model=model_name, error=str(e))
                logger.warning(f"Gemini model {model_name} failed: {e}. Trying next candidate...")

    raise last_err or ValueError("Failed to obtain response from Gemini flash models.")


async def call_groq_fallback(resume_text: str, job_desc: str) -> Tuple[ATSMatchResult, str]:
    """
    Fallback Engine: Groq Free Tier open-weight models using JSON object mode.
    """
    api_key = get_groq_api_key()

    from groq import Groq
    client = Groq(api_key=api_key)

    system_content = f"{SYSTEM_INSTRUCTION}\n\nRespond with valid JSON matching this schema:\n{JSON_SCHEMA_DESCRIPTION}"
    prompt_content = build_user_prompt(resume_text, job_desc)

    candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    last_err = None

    with logfire.span("Groq Failover Engine"):
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
                        data = json.loads(raw_content)
                        logfire.info("Groq failover analysis succeeded", model=model_name)
                        return ATSMatchResult.model_validate(data), f"ATS DeepScan Engine ({model_name})"
            except Exception as e:
                last_err = e
                logfire.warn("Groq model candidate failed", model=model_name, error=str(e))
                logger.warning(f"Groq model {model_name} failed: {e}. Trying next open model...")

    raise last_err or ValueError("Failed to obtain response from Groq models.")


async def analyze_with_fallback(resume_text: str, job_desc: str) -> Tuple[ATSMatchResult, str]:
    """
    Coordinates primary Gemini call with automatic failover to Groq.
    Enforces concurrency limits and returns (ATSMatchResult, white_label_engine_name).
    """
    async with concurrency_semaphore:
        with logfire.span("Dual Engine Match Analysis"):
            # 1. Attempt Primary Engine (Google Gemini)
            try:
                logger.info("Dispatching analysis to primary engine...")
                result = await call_gemini_primary(resume_text, job_desc)
                return result, "ATS DeepScan Engine • Active"
            except Exception as e:
                logger.warning(f"Primary engine call failed: {e}. Routing to failover engine...")
                logfire.warn("Primary engine failed, triggering failover", error=str(e))

            # 2. Attempt Secondary Failover Engine (Groq Open-Weight)
            try:
                logger.info("Dispatching analysis to secondary failover engine...")
                result, _ = await call_groq_fallback(resume_text, job_desc)
                return result, "ATS DeepScan Engine (Failover Mode)"
            except Exception as groq_e:
                logger.error(f"Secondary failover engine call also failed: {groq_e}")
                logfire.error("Secondary failover engine also failed", error=str(groq_e))
                raise RuntimeError(
                    "ATS verification services temporarily unavailable. Please try again shortly."
                )
