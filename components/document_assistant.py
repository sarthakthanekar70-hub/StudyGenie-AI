"""
components/document_assistant.py

Document / PDF Assistant feature.
Supports PDF and TXT only — this is documented accurately, not oversold.
"""

import streamlit as st

from services.gemini_service import analyze_document, answer_document_question, GeminiServiceError
from utils.document_processor import process_uploaded_file, DocumentProcessingError
from utils.validators import validate_uploaded_file
from utils.session_manager import increment_stat, reset_document_session


def render_document_assistant() -> None:
    st.title("📄 Document Assistant")
    st.caption(
        "Upload a PDF or TXT file. StudyGenie extracts the text and can summarize it, "
        "generate notes/questions, or answer questions about its content."
    )

    if st.session_state["document_text"] is None:
        uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt"])

        if uploaded_file is not None:
            valid, error = validate_uploaded_file(uploaded_file)
            if not valid:
                st.error(error)
                return

            with st.spinner("Reading document..."):
                try:
                    file_bytes = uploaded_file.read()
                    text, truncated = process_uploaded_file(file_bytes, uploaded_file.name)
                    st.session_state["document_text"] = text
                    st.session_state["document_name"] = uploaded_file.name
                    st.session_state["document_truncated"] = truncated
                    increment_stat("stats_documents_processed")
                    st.rerun()
                except DocumentProcessingError as e:
                    st.error(str(e))
        return

    # A document is already loaded
    st.success(f"📄 Loaded: {st.session_state['document_name']}")
    if st.session_state["document_truncated"]:
        st.warning(
            "This document was long, so only the first portion of it was used "
            "to keep requests within safe limits."
        )

    if st.button("Remove document / upload a new one"):
        reset_document_session()
        st.rerun()

    st.divider()
    st.subheader("Quick actions")
    col1, col2, col3 = st.columns(3)

    action = None
    if col1.button("Summarize", use_container_width=True):
        action = "summary"
    if col2.button("Generate Notes", use_container_width=True):
        action = "notes"
    if col3.button("Generate Questions", use_container_width=True):
        action = "questions"

    if action:
        with st.spinner("Analyzing document..."):
            try:
                result = analyze_document(st.session_state["document_text"], action)
                st.markdown(result)
            except GeminiServiceError as e:
                st.error(str(e))

    st.divider()
    st.subheader("Ask a question about this document")

    for turn in st.session_state["document_chat_history"]:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])

    question = st.chat_input("e.g. What is process scheduling?")
    if question:
        st.session_state["document_chat_history"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                try:
                    answer = answer_document_question(st.session_state["document_text"], question)
                    st.markdown(answer)
                    st.session_state["document_chat_history"].append(
                        {"role": "assistant", "content": answer}
                    )
                    increment_stat("stats_questions_asked")
                except GeminiServiceError as e:
                    st.error(str(e))
