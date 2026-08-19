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


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes entirely in RAM with strict safety bounds:
    - Validates %PDF- magic header
    - Enforces maximum file size ceiling (120 KB max)
    - Enforces maximum page ceiling (3 pages max)
    - Enforces maximum character ceiling (10,000 chars max)
    """
    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise ValueError(
            f"PDF file size ({len(pdf_bytes) / 1024:.1f} KB) exceeds the maximum allowed limit of {MAX_PDF_SIZE_BYTES // 1024} KB."
        )

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("Invalid file format. Uploaded file is not a valid PDF document.")

    try:
        stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(stream)

        num_pages = len(reader.pages)
        if num_pages == 0:
            raise ValueError("The uploaded PDF has no readable pages.")

        if num_pages > MAX_PDF_PAGES:
            raise ValueError(
                f"PDF has {num_pages} pages. Maximum allowed is {MAX_PDF_PAGES} pages."
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
            raise ValueError(
                "Could not extract any readable text from this PDF. It might be scanned or image-only."
            )

        if len(full_text) > MAX_TEXT_CHARS:
            full_text = full_text[:MAX_TEXT_CHARS]

        return full_text
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise ValueError(f"Failed to process PDF: {str(e)}")
