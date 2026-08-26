"""
components/chat.py

AI Study Chat feature — conversational assistant powered by Gemini.
"""

import streamlit as st

from services.gemini_service import generate_chat_response, GeminiServiceError
from utils.validators import validate_chat_message
from utils.session_manager import reset_chat, increment_stat


def render_chat() -> None:
    st.title("💬 AI Study Chat")
    st.caption("Ask anything academic — concepts, code, math, or follow-up questions.")

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Clear chat", use_container_width=True):
            reset_chat()
            st.rerun()

    if not st.session_state["chat_history"]:
        st.info(
            "💡 Try asking: *\"Explain machine learning in simple words.\"* "
            "Then follow up with *\"Give me an example.\"*"
        )

    for turn in st.session_state["chat_history"]:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])

    user_message = st.chat_input("Ask a question...")

    if user_message:
        valid, error = validate_chat_message(user_message)
        if not valid:
            st.error(error)
            return

        st.session_state["chat_history"].append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    style = st.session_state.get("response_style", "Simple")
                    reply = generate_chat_response(
                        st.session_state["chat_history"][:-1],
                        user_message,
                        style,
                    )
                    st.markdown(reply)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                    increment_stat("stats_questions_asked")
                except GeminiServiceError as e:
                    st.error(str(e))
