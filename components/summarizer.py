"""
components/summarizer.py

Text Summarizer feature.
"""

import streamlit as st

from config.settings import SUMMARY_TYPES, MAX_SUMMARY_INPUT_CHARS
from services.gemini_service import summarize_text, GeminiServiceError
from utils.validators import validate_summary_text


def render_summarizer() -> None:
    st.title("📝 Text Summarizer")
    st.caption("Paste academic text and get a structured summary.")

    text = st.text_area(
        "Paste your text here",
        height=250,
        placeholder="Paste a paragraph, article, or notes to summarize (e.g. a textbook chapter excerpt)...",
        max_chars=MAX_SUMMARY_INPUT_CHARS,
    )
    st.caption(f"{len(text)} / {MAX_SUMMARY_INPUT_CHARS} characters")

    summary_type = st.selectbox("Summary type", SUMMARY_TYPES)

    if st.button("Summarize", use_container_width=True):
        valid, error = validate_summary_text(text)
        if not valid:
            st.error(error)
            return

        with st.spinner("Summarizing..."):
            try:
                result = summarize_text(text, summary_type)
                st.markdown("### Summary")
                st.markdown(result)
                st.text_area(
                    "Copy-friendly output",
                    value=result,
                    height=200,
                    help="Select all and copy this text.",
                )
            except GeminiServiceError as e:
                st.error(str(e))
