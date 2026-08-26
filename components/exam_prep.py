"""
components/exam_prep.py

Exam Preparation feature.
"""

import streamlit as st

from config.settings import DIFFICULTY_LEVELS, EXAM_TYPES, MIN_EXAM_QUESTIONS, MAX_EXAM_QUESTIONS
from services.gemini_service import generate_exam_prep, GeminiServiceError
from utils.validators import validate_exam_prep_inputs


def render_exam_prep() -> None:
    st.title("🎯 Exam Preparation")
    st.caption("Generate a structured exam preparation package for your subject.")

    with st.form("exam_prep_form"):
        subject = st.text_input("Subject", placeholder="e.g. Data Structures")
        chapters = st.text_area(
            "Chapters / topics to cover",
            placeholder="e.g. Arrays, Linked Lists, Stacks, Queues",
        )
        col1, col2 = st.columns(2)
        with col1:
            exam_type = st.selectbox("Exam type", EXAM_TYPES)
        with col2:
            difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS)

        num_questions = st.slider(
            "Approximate number of practice questions",
            min_value=MIN_EXAM_QUESTIONS,
            max_value=MAX_EXAM_QUESTIONS,
            value=10,
        )

        submitted = st.form_submit_button("Generate Exam Prep", use_container_width=True)

    if submitted:
        valid, error = validate_exam_prep_inputs(subject, chapters, num_questions)
        if not valid:
            st.error(error)
            return

        with st.spinner("Building your exam preparation package..."):
            try:
                result = generate_exam_prep(subject, chapters, exam_type, difficulty, num_questions)
                st.markdown(result)
                st.download_button(
                    "Download as Markdown",
                    data=result,
                    file_name=f"{subject.strip().replace(' ', '_')}_exam_prep.md",
                    mime="text/markdown",
                )
            except GeminiServiceError as e:
                st.error(str(e))
