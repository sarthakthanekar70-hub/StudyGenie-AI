"""
utils/session_manager.py

Helper functions for initializing and updating Streamlit session state.
No permanent storage — everything here is session-scoped by design.
"""

import streamlit as st


def init_session_state() -> None:
    """Initialize all session state keys used across the app, if not already set."""

    defaults = {
        # Navigation
        "current_page": "Dashboard",

        # Chat
        "chat_history": [],  # list of {"role": "user"/"assistant", "content": str}

        # Document assistant
        "document_text": None,
        "document_name": None,
        "document_truncated": False,
        "document_chat_history": [],

        # Quiz / MCQ state
        "quiz_data": None,
        "quiz_answers": {},
        "quiz_submitted": False,

        # Session statistics (dashboard) — session-based only, never fabricated
        "stats_questions_asked": 0,
        "stats_notes_generated": 0,
        "stats_documents_processed": 0,
        "stats_mcqs_generated": 0,

        # Settings
        "response_style": "Simple",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def increment_stat(stat_key: str, amount: int = 1) -> None:
    """Increment a session statistic counter safely."""
    current = st.session_state.get(stat_key, 0)
    st.session_state[stat_key] = current + amount


def reset_chat() -> None:
    st.session_state["chat_history"] = []


def reset_document_session() -> None:
    st.session_state["document_text"] = None
    st.session_state["document_name"] = None
    st.session_state["document_truncated"] = False
    st.session_state["document_chat_history"] = []


def reset_quiz() -> None:
    st.session_state["quiz_data"] = None
    st.session_state["quiz_answers"] = {}
    st.session_state["quiz_submitted"] = False
