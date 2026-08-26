"""
components/sidebar.py

Sidebar navigation for StudyGenie AI.
"""

import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from services.gemini_service import is_configured

PAGES = [
    "🏠 Dashboard",
    "💬 AI Study Chat",
    "📚 Explain Topic",
    "📝 Summarizer",
    "🧠 MCQ Generator",
    "📖 Study Notes",
    "📄 Document Assistant",
    "🎯 Exam Preparation",
    "⚙️ Settings",
    "ℹ️ About",
]


def render_sidebar() -> str:
    """Render the sidebar and return the selected page label."""
    with st.sidebar:
        st.markdown(f"### 🧞 {APP_NAME}")
        st.caption(APP_TAGLINE)
        st.divider()

        selected = st.radio(
            "Navigation",
            PAGES,
            label_visibility="collapsed",
            key="nav_radio",
        )

        st.divider()

        if is_configured():
            st.success("Gemini API: Connected", icon="✅")
        else:
            st.error("Gemini API: Not configured", icon="⚠️")
            st.caption("Set GEMINI_API_KEY to enable AI features.")

        st.caption(f"v{st.session_state.get('app_version', '1.0.0')}")

    return selected
