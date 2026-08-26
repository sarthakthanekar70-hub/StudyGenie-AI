"""
components/dashboard.py

Dashboard / home page for StudyGenie AI.
"""

import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE


FEATURE_CARDS = [
    ("💬", "AI Chat", "Ask academic, coding, or math questions and get clear, contextual answers."),
    ("📚", "Explain Topics", "Get structured explanations at your chosen difficulty level."),
    ("📝", "Summarize", "Turn long academic text into short or exam-ready summaries."),
    ("🧠", "Generate MCQs", "Create practice quizzes on any topic in seconds."),
    ("📖", "Create Notes", "Generate structured, revision-ready study notes."),
    ("📄", "Analyze Documents", "Upload a PDF and ask questions about its content."),
]


def render_dashboard() -> None:
    st.title(f"Welcome to {APP_NAME}")
    st.markdown(f"##### {APP_TAGLINE}")
    st.write("")

    cols = st.columns(3)
    for idx, (icon, title, desc) in enumerate(FEATURE_CARDS):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(desc)

    st.write("")
    st.subheader("📊 This Session")
    st.caption("These statistics are session-based and reset when you close or refresh the app.")

    stat_cols = st.columns(4)
    stat_cols[0].metric("Questions Asked", st.session_state.get("stats_questions_asked", 0))
    stat_cols[1].metric("Notes Generated", st.session_state.get("stats_notes_generated", 0))
    stat_cols[2].metric("Documents Processed", st.session_state.get("stats_documents_processed", 0))
    stat_cols[3].metric("MCQ Sets Generated", st.session_state.get("stats_mcqs_generated", 0))
