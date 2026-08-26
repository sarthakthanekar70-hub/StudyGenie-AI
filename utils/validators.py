"""
utils/validators.py

Validation helpers for user inputs across all StudyGenie AI features.
Each function returns (is_valid: bool, error_message: str).
An empty error_message means the input is valid.
"""

from typing import Tuple

from config.settings import (
    MIN_SUMMARY_INPUT_CHARS,
    MAX_SUMMARY_INPUT_CHARS,
    MIN_MCQ_COUNT,
    MAX_MCQ_COUNT,
    MIN_EXAM_QUESTIONS,
    MAX_EXAM_QUESTIONS,
    MAX_PDF_SIZE_MB,
)


def validate_non_empty(value: str, field_name: str = "This field") -> Tuple[bool, str]:
    if not value or not value.strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_chat_message(message: str) -> Tuple[bool, str]:
    if not message or not message.strip():
        return False, "Please type a message before sending."
    if len(message) > 4000:
        return False, "Your message is too long. Please shorten it."
    return True, ""


def validate_topic(topic: str) -> Tuple[bool, str]:
    return validate_non_empty(topic, "Topic")


def validate_summary_text(text: str) -> Tuple[bool, str]:
    if not text or not text.strip():
        return False, "Please paste some text to summarize."
    if len(text) < MIN_SUMMARY_INPUT_CHARS:
        return False, f"Please provide at least {MIN_SUMMARY_INPUT_CHARS} characters of text."
    if len(text) > MAX_SUMMARY_INPUT_CHARS:
        return False, (
            f"Your text is too long ({len(text)} characters). "
            f"Please limit it to {MAX_SUMMARY_INPUT_CHARS} characters."
        )
    return True, ""


def validate_mcq_inputs(topic: str, count: int, subject: str) -> Tuple[bool, str]:
    valid, msg = validate_non_empty(topic, "Topic")
    if not valid:
        return valid, msg
    valid, msg = validate_non_empty(subject, "Subject")
    if not valid:
        return valid, msg
    if not (MIN_MCQ_COUNT <= count <= MAX_MCQ_COUNT):
        return False, f"Number of questions must be between {MIN_MCQ_COUNT} and {MAX_MCQ_COUNT}."
    return True, ""


def validate_notes_inputs(subject: str, topic: str) -> Tuple[bool, str]:
    valid, msg = validate_non_empty(subject, "Subject")
    if not valid:
        return valid, msg
    return validate_non_empty(topic, "Topic")


def validate_exam_prep_inputs(subject: str, chapters: str, num_questions: int) -> Tuple[bool, str]:
    valid, msg = validate_non_empty(subject, "Subject")
    if not valid:
        return valid, msg
    valid, msg = validate_non_empty(chapters, "Chapters")
    if not valid:
        return valid, msg
    if not (MIN_EXAM_QUESTIONS <= num_questions <= MAX_EXAM_QUESTIONS):
        return False, (
            f"Number of questions must be between {MIN_EXAM_QUESTIONS} and {MAX_EXAM_QUESTIONS}."
        )
    return True, ""


def validate_uploaded_file(file) -> Tuple[bool, str]:
    """Validate a Streamlit UploadedFile object before processing."""
    if file is None:
        return False, "Please upload a file."

    size_mb = file.size / (1024 * 1024)
    if size_mb > MAX_PDF_SIZE_MB:
        return False, f"File is too large ({size_mb:.1f} MB). Maximum allowed is {MAX_PDF_SIZE_MB} MB."

    name_lower = file.name.lower()
    if not (name_lower.endswith(".pdf") or name_lower.endswith(".txt")):
        return False, "Unsupported file type. Please upload a PDF or TXT file."

    return True, ""
