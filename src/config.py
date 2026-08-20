"""
Configuration settings and system constants for ATS MatchProof.
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# System Constraints & Boundaries
MAX_PDF_SIZE_BYTES: int = 120 * 1024  # 120 KB max
MAX_PDF_PAGES: int = 3  # 3 pages max
MAX_TEXT_CHARS: int = 7000  # 7,000 characters with spaces max

# Rate Limiting & Concurrency Policies
rate_per_min = os.getenv("RATE_LIMIT_PER_MINUTE", "2")
RATE_LIMIT_POLICY: str = os.getenv("RATE_LIMIT_POLICY", f"{rate_per_min}/minute")
MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "3"))


# API Keys (Loaded from environment)
def get_gemini_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not configured or contains placeholder.")
    return key


def get_groq_api_key() -> str:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key or key == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY is not configured or contains placeholder.")
    return key


# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ats_matcher")
