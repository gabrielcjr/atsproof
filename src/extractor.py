"""
In-memory PDF text extraction and validation.
Strictly ephemeral: no files are saved to disk.
"""

import io
import re

from pypdf import PdfReader

from src.config import (
    MAX_PDF_PAGES,
    MAX_PDF_SIZE_BYTES,
    MAX_TEXT_CHARS,
    logger,
)
from src.i18n import get_translations


def extract_text_from_pdf_bytes(pdf_bytes: bytes, lang: str = "en") -> str:
    """
    Extracts text from PDF bytes entirely in RAM with strict safety bounds:
    - Validates %PDF- magic header
    - Enforces maximum file size ceiling (200 KB max)
    - Enforces maximum page ceiling (3 pages max)
    - Enforces maximum character ceiling (7,000 chars max)
    """
    t = get_translations(lang)

    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise ValueError(
            t["error_pdf_size"].format(
                size_kb=len(pdf_bytes) / 1024, max_kb=MAX_PDF_SIZE_BYTES // 1024
            )
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError(t["error_pdf_invalid"])

    try:
        stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(stream)

        num_pages = len(reader.pages)
        if num_pages == 0:
            raise ValueError(t["error_pdf_no_pages"])

        if num_pages > MAX_PDF_PAGES:
            raise ValueError(
                t["error_pdf_max_pages"].format(
                    num_pages=num_pages, max_pages=MAX_PDF_PAGES
                )
            )

        extracted_text_parts = []
        for page_idx in range(min(num_pages, MAX_PDF_PAGES)):
            page = reader.pages[page_idx]
            page_text = page.extract_text() or ""
            extracted_text_parts.append(page_text)

        full_text = "\n".join(extracted_text_parts).strip()

        # Clean null bytes and excessive whitespace
        full_text = full_text.replace("\x00", " ")
        full_text = re.sub(r"[ \t]+", " ", full_text)
        full_text = re.sub(r"\n{3,}", "\n\n", full_text)

        if not full_text:
            raise ValueError(t["error_pdf_no_text"])

        if len(full_text) > MAX_TEXT_CHARS:
            full_text = full_text[:MAX_TEXT_CHARS]

        return full_text
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise ValueError(t["error_pdf_process"])
