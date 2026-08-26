"""
About & Project Information Page for StudyGenie AI
"""
import streamlit as st
from config.settings import APP_NAME, APP_TAGLINE, APP_VERSION, MODEL_NAME
def render_about():
    """Render StudyGenie About & Information page."""
    st.title(f"ℹ️ About {APP_NAME}")
    st.caption(f"Version {VERSION} | {APP_TAGLINE}")
    st.markdown("---")
    st.markdown(
        """
        ### 🎯 Project Overview
        **StudyGenie AI** is an intelligent, AI-powered academic assistant engineered to revolutionize student learning.
        Built with **Python**, **Streamlit**, and the official **Google Gemini API** (`google-genai` SDK), StudyGenie AI empowers students to:
        - 💬 **Ask Academic Questions**: Multi-turn conversational study chat with context preservation.
        - 📚 **Master Difficult Topics**: Multi-level conceptual breakdowns tailored to Beginner, Intermediate, or Advanced levels.
        - 📝 **Summarize Study Material**: Transform lengthy textbook passages into actionable revision notes.
        - 🧠 **Interactive MCQ Testing**: Generate custom quizzes with interactive scoring and rationale breakdowns.
        - 📖 **Craft Revision Study Notes**: Automated markdown study guides with key definitions and high-yield points.
        - 📄 **Analyze PDF Study Documents**: Extract, clean, summarize, and query PDF lecture slides and textbooks using `pypdf`.
        - 🎯 **Conquer Examinations**: Generate exam strategies, high-yield practice questions, and structured revision plans.
        ---
        ### 🛠️ Technology Stack
        - **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
        - **AI Engine & SDK**: [Google Gemini API](https://ai.google.dev/) via `google-genai` Python SDK
        - **PDF Processing**: `pypdf`
        - **Configuration & Environment**: `python-dotenv` & `.streamlit/config.toml`
        ---
        ### 🔑 API Key & Security Setup
        StudyGenie AI strictly respects user key security:
        1. **Environment Variable**: Set `GEMINI_API_KEY=your_key` in a `.env` file.
        2. **Streamlit Secrets**: Add `GEMINI_API_KEY = "your_key"` to `.streamlit/secrets.toml`.
        3. **UI Setting**: Override or paste your key directly in **⚙️ Settings** tab.
        
        *Note: Secrets and `.env` files are ignored by git in `.gitignore` to prevent secret exposure.*
        ---
        ### 📜 License & Credits
        - Developed as part of the Google Skills Lab activity: *"Develop Gen AI Apps with Gemini and Streamlit"*
        - Released under the **MIT License**.
        """
    )
