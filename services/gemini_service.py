"""
services/gemini_service.py

Central Gemini API integration layer for StudyGenie AI.
Every feature in the app calls into this module rather than touching the
google-genai SDK directly. This keeps client init, error handling, and
generation config in one place.
"""

import json
import os
import re
from typing import Dict, List, Optional

import streamlit as st
from google import genai
from google.genai import types

from config.settings import MODEL_NAME, GENERATION_CONFIGS
from utils import prompts as prompt_lib


class GeminiServiceError(Exception):
    """User-facing error raised for any Gemini-related failure."""
    pass


# ---------------------------------------------------------------------------
# API key loading
# ---------------------------------------------------------------------------
def _load_api_key() -> Optional[str]:
    """
    Load the Gemini API key from environment variables first, then from
    Streamlit secrets (for Streamlit Community Cloud deployment).
    Never hard-coded, never logged.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        # st.secrets raises if no secrets.toml exists at all — that's fine locally.
        pass

    return None


@st.cache_resource(show_spinner=False)
def _get_client() -> "genai.Client":
    """
    Create (and cache) a single Gemini client for the app session.
    Raises GeminiServiceError with a clear message if the key is missing.
    """
    api_key = _load_api_key()
    if not api_key:
        raise GeminiServiceError(
            "Gemini API key is not configured. Please configure GEMINI_API_KEY."
        )
    try:
        return genai.Client(api_key=api_key)
    except Exception as exc:
        raise GeminiServiceError(
            "Could not initialize the Gemini client. Please check your API key."
        ) from exc


def is_configured() -> bool:
    """Check whether a Gemini API key is available, without raising."""
    return _load_api_key() is not None


# ---------------------------------------------------------------------------
# Low-level call wrapper — every feature function routes through this
# ---------------------------------------------------------------------------
def _call_gemini(prompt: str, config_preset: str = "chat") -> str:
    """
    Send a prompt to Gemini and return the text response.
    Raises GeminiServiceError with a user-friendly message on any failure.
    """
    client = _get_client()
    gen_cfg = GENERATION_CONFIGS.get(config_preset, GENERATION_CONFIGS["chat"])

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=gen_cfg["temperature"],
                max_output_tokens=gen_cfg["max_output_tokens"],
            ),
        )
    except Exception as exc:
        # TEMPORARY DEBUG LOGGING — prints the real error to your terminal
        # (not to the browser). Safe to remove once things are working.
        print(f"\n[DEBUG] Gemini call failed: {type(exc).__name__}: {exc}\n")

        message = str(exc).lower()
        if "api key" in message or "unauthorized" in message or "permission" in message:
            raise GeminiServiceError(
                "Your Gemini API key appears to be invalid or unauthorized. "
                "Please check GEMINI_API_KEY."
            ) from exc
        if "quota" in message or "rate" in message or "429" in message:
            raise GeminiServiceError(
                "Gemini API rate limit or quota exceeded. Please wait a moment and try again."
            ) from exc
        if "timeout" in message or "connection" in message or "network" in message:
            raise GeminiServiceError(
                "A network error occurred while contacting Gemini. Please try again."
            ) from exc
        if "not found" in message or "404" in message:
            raise GeminiServiceError(
                f"The configured Gemini model ('{MODEL_NAME}') was not found or is "
                "unavailable for your API key. Please check MODEL_NAME in config/settings.py."
            ) from exc

        raise GeminiServiceError(
            "Something went wrong while generating a response. Please try again."
        ) from exc

    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise GeminiServiceError(
            "Gemini did not return any content for this request. "
            "Please try rephrasing your input."
        )

    return text.strip()


def _extract_json(raw_text: str) -> Dict:
    """
    Defensively extract a JSON object from a model response, in case the
    model wraps it in markdown code fences despite instructions not to.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to locate the first { ... last } as a fallback
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start:end + 1])
            except json.JSONDecodeError as exc:
                raise GeminiServiceError(
                    "Gemini returned an unexpected response format. Please try again."
                ) from exc
        raise GeminiServiceError(
            "Gemini returned an unexpected response format. Please try again."
        )


# ---------------------------------------------------------------------------
# Feature 1 — Chat
# ---------------------------------------------------------------------------
def generate_chat_response(history: List[Dict[str, str]], user_message: str, style: str = "Simple") -> str:
    prompt = prompt_lib.build_chat_prompt(history, user_message, style)
    return _call_gemini(prompt, config_preset="chat")


# ---------------------------------------------------------------------------
# Feature 2 — Explain a Topic
# ---------------------------------------------------------------------------
def explain_topic(topic: str, difficulty: str, style: str) -> str:
    prompt = prompt_lib.build_topic_prompt(topic, difficulty, style)
    return _call_gemini(prompt, config_preset="creative_explanation")


# ---------------------------------------------------------------------------
# Feature 3 — Summarizer
# ---------------------------------------------------------------------------
def summarize_text(text: str, summary_type: str) -> str:
    prompt = prompt_lib.build_summary_prompt(text, summary_type)
    return _call_gemini(prompt, config_preset="chat")


# ---------------------------------------------------------------------------
# Feature 4 — MCQ Generator
# ---------------------------------------------------------------------------
def generate_mcqs(topic: str, count: int, difficulty: str, subject: str) -> List[Dict]:
    prompt = prompt_lib.build_mcq_prompt(topic, count, difficulty, subject)
    raw = _call_gemini(prompt, config_preset="structured_json")
    data = _extract_json(raw)

    questions = data.get("questions")
    if not isinstance(questions, list) or len(questions) == 0:
        raise GeminiServiceError(
            "Gemini did not return any valid questions. Please try again."
        )
    return questions


# ---------------------------------------------------------------------------
# Feature 5 — Study Notes Generator
# ---------------------------------------------------------------------------
def generate_notes(subject: str, topic: str, level: str, length: str) -> str:
    prompt = prompt_lib.build_notes_prompt(subject, topic, level, length)
    return _call_gemini(prompt, config_preset="notes")


# ---------------------------------------------------------------------------
# Feature 6 — Document Assistant
# ---------------------------------------------------------------------------
def analyze_document(document_text: str, mode: str) -> str:
    """mode is one of: 'summary', 'notes', 'questions'."""
    prompt = prompt_lib.build_document_summary_prompt(document_text, mode)
    return _call_gemini(prompt, config_preset="document_qa")


def answer_document_question(document_text: str, question: str) -> str:
    prompt = prompt_lib.build_document_qa_prompt(document_text, question)
    return _call_gemini(prompt, config_preset="document_qa")


# ---------------------------------------------------------------------------
# Feature 7 — Exam Preparation
# ---------------------------------------------------------------------------
def generate_exam_prep(subject: str, chapters: str, exam_type: str,
                        difficulty: str, num_questions: int) -> str:
    prompt = prompt_lib.build_exam_prep_prompt(subject, chapters, exam_type, difficulty, num_questions)
    return _call_gemini(prompt, config_preset="structured_json")