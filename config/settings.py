"""
config/settings.py

Central configuration for StudyGenie AI.
No secrets live here — only non-sensitive application/model configuration.
"""

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "StudyGenie AI"
APP_TAGLINE = "Learn smarter with Gemini."
APP_VERSION = "1.0.0"
VERSION = APP_VERSION
AUTHOR = "Sarthak"

# ---------------------------------------------------------------------------
# Gemini model configuration
# ---------------------------------------------------------------------------
# Centralized so the model can be swapped in exactly one place.
MODEL_NAME = "gemini-3.7-flash"
# Named generation-config presets used across features.
# Keeping these centralized avoids "magic numbers" scattered through the code.
GENERATION_CONFIGS = {
    "chat": {
        "temperature": 0.7,
        "max_output_tokens": 1024,
    },
    "creative_explanation": {
        "temperature": 0.6,
        "max_output_tokens": 1536,
    },
    "structured_json": {
        # Lower temperature -> more consistent, parseable JSON output
        "temperature": 0.3,
        "max_output_tokens": 2048,
    },
    "notes": {
        "temperature": 0.4,
        "max_output_tokens": 2048,
    },
    "document_qa": {
        "temperature": 0.3,
        "max_output_tokens": 1536,
    },
}

# ---------------------------------------------------------------------------
# Document / upload limits
# ---------------------------------------------------------------------------
MAX_PDF_SIZE_MB = 10
MAX_PDF_PAGES = 60
# Approx. character budget sent to Gemini as context from an uploaded document.
# This prevents unbounded / unsafe prompt sizes.
MAX_DOCUMENT_CHARS = 30000

# ---------------------------------------------------------------------------
# Text input limits (summarizer, chat, etc.)
# ---------------------------------------------------------------------------
MAX_SUMMARY_INPUT_CHARS = 20000
MIN_SUMMARY_INPUT_CHARS = 20

# ---------------------------------------------------------------------------
# MCQ / Exam prep limits
# ---------------------------------------------------------------------------
MIN_MCQ_COUNT = 1
MAX_MCQ_COUNT = 20

MIN_EXAM_QUESTIONS = 3
MAX_EXAM_QUESTIONS = 30

# ---------------------------------------------------------------------------
# UI options shared across features
# ---------------------------------------------------------------------------
DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

EXPLANATION_STYLES = [
    "Simple",
    "Detailed",
    "Exam-oriented",
    "Real-world example",
]

RESPONSE_STYLES = [
    "Simple",
    "Professional",
    "Exam-focused",
    "Detailed",
    "Concise",
    "Step-by-step",
]

SUMMARY_TYPES = [
    "Short summary",
    "Detailed summary",
    "Bullet-point notes",
    "Exam revision notes",
]

EXAM_TYPES = [
    "Unit Test",
    "Semester Exam",
    "Competitive Exam",
    "Viva / Oral",
]
