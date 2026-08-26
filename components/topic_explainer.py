"""
components/topic_explainer.py

Explain a Topic feature.
"""

import streamlit as st

from config.settings import DIFFICULTY_LEVELS, EXPLANATION_STYLES
from services.gemini_service import explain_topic, GeminiServiceError
from utils.validators import validate_topic
from utils.session_manager import increment_stat


def render_topic_explainer() -> None:
    st.title("📚 Explain a Topic")
    st.caption("Get a structured explanation of any academic or technical topic.")

    with st.form("topic_form"):
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Binary Search Trees",
        )
        col1, col2 = st.columns(2)
        with col1:
            difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS)
        with col2:
            style = st.selectbox("Explanation style", EXPLANATION_STYLES)

        submitted = st.form_submit_button("Explain Topic", use_container_width=True)

    if submitted:
        valid, error = validate_topic(topic)
        if not valid:
            st.error(error)
            return

        with st.spinner("Generating explanation..."):
            try:
                result = explain_topic(topic, difficulty, style)
                st.markdown(result)
                increment_stat("stats_questions_asked")
            except GeminiServiceError as e:
                st.error(str(e))
