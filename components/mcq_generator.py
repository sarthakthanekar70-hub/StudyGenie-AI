"""
components/mcq_generator.py

MCQ Generator feature with an interactive quiz flow.
"""

import streamlit as st

from config.settings import DIFFICULTY_LEVELS, MIN_MCQ_COUNT, MAX_MCQ_COUNT
from services.gemini_service import generate_mcqs, GeminiServiceError
from utils.validators import validate_mcq_inputs
from utils.session_manager import increment_stat, reset_quiz


def _render_quiz() -> None:
    questions = st.session_state["quiz_data"]

    with st.form("quiz_form"):
        for idx, q in enumerate(questions):
            st.markdown(f"**Q{idx + 1}. {q['question']}**")
            option_labels = [f"{k}. {v}" for k, v in q["options"].items()]
            choice = st.radio(
                f"quiz_q_{idx}",
                option_labels,
                key=f"quiz_choice_{idx}",
                label_visibility="collapsed",
            )
            st.session_state["quiz_answers"][idx] = choice[0] if choice else None
            st.write("")

        submitted = st.form_submit_button("Submit Quiz", use_container_width=True)

    if submitted:
        st.session_state["quiz_submitted"] = True

    if st.session_state["quiz_submitted"]:
        score = 0
        for idx, q in enumerate(questions):
            user_answer = st.session_state["quiz_answers"].get(idx)
            correct = q["correct_option"]
            is_correct = user_answer == correct
            if is_correct:
                score += 1
                st.success(f"Q{idx + 1}: Correct! ({correct}) — {q['explanation']}")
            else:
                st.error(
                    f"Q{idx + 1}: Incorrect. You chose {user_answer or 'nothing'}, "
                    f"correct answer is {correct}. {q['explanation']}"
                )
        st.markdown(f"### Score: {score} / {len(questions)}")

    if st.button("Generate a new quiz"):
        reset_quiz()
        st.rerun()


def render_mcq_generator() -> None:
    st.title("🧠 MCQ Generator")
    st.caption("Generate and take a practice quiz on any topic.")

    if st.session_state["quiz_data"] is None:
        with st.form("mcq_form"):
            topic = st.text_input("Topic", placeholder="e.g. Python Functions")
            subject = st.text_input("Subject", placeholder="e.g. Programming")
            col1, col2 = st.columns(2)
            with col1:
                count = st.number_input(
                    "Number of questions",
                    min_value=MIN_MCQ_COUNT,
                    max_value=MAX_MCQ_COUNT,
                    value=5,
                )
            with col2:
                difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS)

            submitted = st.form_submit_button("Generate MCQs", use_container_width=True)

        if submitted:
            valid, error = validate_mcq_inputs(topic, int(count), subject)
            if not valid:
                st.error(error)
                return

            with st.spinner("Generating questions..."):
                try:
                    questions = generate_mcqs(topic, int(count), difficulty, subject)
                    st.session_state["quiz_data"] = questions
                    st.session_state["quiz_answers"] = {}
                    st.session_state["quiz_submitted"] = False
                    increment_stat("stats_mcqs_generated")
                    st.rerun()
                except GeminiServiceError as e:
                    st.error(str(e))
    else:
        _render_quiz()
