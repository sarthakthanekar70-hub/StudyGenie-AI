"""
utils/document_processor.py

Handles PDF (and plain text) extraction, cleaning, and safe length limiting.
Only PDF and TXT are actually supported — no format is claimed beyond that.
"""

import io
import re
from typing import Tuple

from pypdf import PdfReader

from config.settings import MAX_DOCUMENT_CHARS, MAX_PDF_PAGES


class DocumentProcessingError(Exception):
    """Raised when a document cannot be safely processed."""
    pass


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file's raw bytes.
    Raises DocumentProcessingError on invalid/corrupted PDFs.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except Exception as exc:
        raise DocumentProcessingError(
            "This file could not be read as a valid PDF. Please upload a valid PDF document."
        ) from exc

    if len(reader.pages) == 0:
        raise DocumentProcessingError("The uploaded PDF appears to be empty.")

    if len(reader.pages) > MAX_PDF_PAGES:
        raise DocumentProcessingError(
            f"This PDF has {len(reader.pages)} pages, which exceeds the "
            f"{MAX_PDF_PAGES}-page limit. Please upload a shorter document."
        )

    text_parts = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        text_parts.append(page_text)

    full_text = "\n".join(text_parts)

    if not full_text.strip():
        raise DocumentProcessingError(
            "No extractable text was found in this PDF. It may be a scanned "
            "image-only document, which isn't supported yet."
        )

    return full_text


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode a plain text file safely."""
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception as exc:
        raise DocumentProcessingError("This text file could not be read.") from exc


def clean_text(text: str) -> str:
    """Basic whitespace normalization for extracted document text."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def truncate_text(text: str, max_chars: int = MAX_DOCUMENT_CHARS) -> Tuple[str, bool]:
    """
    Truncate text to a safe character budget.
    Returns (truncated_text, was_truncated).
    """
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars], True


def process_uploaded_file(file_bytes: bytes, filename: str) -> Tuple[str, bool]:
    """
    Full pipeline: extract -> clean -> truncate.
    Returns (final_text, was_truncated).
    Raises DocumentProcessingError for unsupported or invalid files.
    """
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
    elif lower_name.endswith(".txt"):
        raw_text = extract_text_from_txt(file_bytes)
    else:
        raise DocumentProcessingError(
            "Unsupported file type. Please upload a PDF or TXT file."
        )

    cleaned = clean_text(raw_text)
    final_text, was_truncated = truncate_text(cleaned)
    return final_text, was_truncated
