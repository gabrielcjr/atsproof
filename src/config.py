"""
Configuration settings and system constants for ATS MatchProof.
"""

import ipaddress
import logging
import os
from functools import lru_cache
from typing import Tuple

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# System Constraints & Boundaries
MAX_PDF_SIZE_BYTES: int = 200 * 1024  # 200 KB max
MAX_PDF_PAGES: int = 3  # 3 pages max
MAX_TEXT_CHARS: int = 7000  # 7,000 characters with spaces max
MAX_REQUEST_BODY_BYTES: int = int(os.getenv("MAX_REQUEST_BODY_BYTES", str(512 * 1024)))

# Rate Limiting & Concurrency Policies
rate_per_min = os.getenv("RATE_LIMIT_PER_MINUTE", "2")
RATE_LIMIT_POLICY: str = os.getenv("RATE_LIMIT_POLICY", f"{rate_per_min}/minute")
RATE_LIMIT_STORAGE_URI: str = os.getenv("RATE_LIMIT_STORAGE_URI", "memory://")
TRUSTED_PROXY_IPS: str = os.getenv(
    "TRUSTED_PROXY_IPS", "127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
)
MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "3"))
LLM_CALL_TIMEOUT_SECONDS: float = float(os.getenv("LLM_CALL_TIMEOUT_SECONDS", "25.0"))
SEMAPHORE_TIMEOUT_SECONDS: float = float(os.getenv("SEMAPHORE_TIMEOUT_SECONDS", "15.0"))
ANALYSIS_TOTAL_TIMEOUT_SECONDS: float = float(
    os.getenv("ANALYSIS_TOTAL_TIMEOUT_SECONDS", "45.0")
)


@lru_cache(maxsize=8)
def _parse_trusted_proxy_networks(
    raw: str,
) -> Tuple[ipaddress._BaseNetwork, ...]:
    """Parses comma-separated CIDR/IP entries into ip_network objects."""
    networks = []
    for entry in (raw or "").split(","):
        cleaned = entry.strip()
        if not cleaned:
            continue
        try:
            networks.append(ipaddress.ip_network(cleaned, strict=False))
        except ValueError:
            continue
    return tuple(networks)


def is_trusted_proxy(host: str) -> bool:
    """Returns True if host is a valid IP inside TRUSTED_PROXY_IPS."""
    if not host:
        return False
    try:
        addr = ipaddress.ip_address(host.strip())
    except ValueError:
        return False
    return any(addr in net for net in _parse_trusted_proxy_networks(TRUSTED_PROXY_IPS))


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
