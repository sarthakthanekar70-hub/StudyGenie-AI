"""
components/notes_generator.py

Study Notes Generator feature.
"""

import streamlit as st

from config.settings import DIFFICULTY_LEVELS
from services.gemini_service import generate_notes, GeminiServiceError
from utils.validators import validate_notes_inputs
from utils.session_manager import increment_stat

LENGTH_OPTIONS = ["Short", "Medium", "Detailed"]


def render_notes_generator() -> None:
    st.title("📖 Study Notes Generator")
    st.caption("Generate structured, revision-ready notes on any topic.")

    with st.form("notes_form"):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Subject", placeholder="e.g. Operating Systems")
        with col2:
            topic = st.text_input("Topic", placeholder="e.g. Process Scheduling")

        col3, col4 = st.columns(2)
        with col3:
            level = st.selectbox("Academic level", DIFFICULTY_LEVELS)
        with col4:
            length = st.selectbox("Desired length", LENGTH_OPTIONS)

        submitted = st.form_submit_button("Generate Notes", use_container_width=True)

    if submitted:
        valid, error = validate_notes_inputs(subject, topic)
        if not valid:
            st.error(error)
            return

        with st.spinner("Generating notes..."):
            try:
                notes = generate_notes(subject, topic, level, length)
                st.markdown(notes)
                increment_stat("stats_notes_generated")
                st.download_button(
                    "Download notes as Markdown",
                    data=notes,
                    file_name=f"{topic.strip().replace(' ', '_')}_notes.md",
                    mime="text/markdown",
                )
            except GeminiServiceError as e:
                st.error(str(e))
