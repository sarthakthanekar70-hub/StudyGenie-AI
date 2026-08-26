# StudyGenie AI

**Learn smarter with Gemini.**

An AI-powered study assistant built with **Google Gemini** and **Streamlit** for the Google Skills Lab activity *"Develop Gen AI Apps with Gemini and Streamlit."*

---

## Overview

StudyGenie AI helps diploma, engineering, and college students understand, summarize, revise, and practice academic topics using Google's Gemini models. It brings together chat, topic explanation, summarization, quiz generation, notes generation, document Q&A, and exam preparation into one clean, modular Streamlit application.

## Problem Statement

Students juggling multiple subjects often need quick, reliable help to:
- Understand a new concept at the right difficulty level
- Condense long text into revision-ready notes
- Practice with quiz questions before an exam
- Extract answers from lecture PDFs without re-reading the whole document

Doing this manually, or across many disconnected tools, is slow and inconsistent.

## Solution

StudyGenie AI centralizes these workflows into a single Gemini-powered interface: one consistent design, one consistent way prompts are built, and one consistent way errors are handled — so the AI experience feels reliable across every feature.

## Objectives

- Demonstrate a real, working Generative AI application (not a toy demo)
- Use Gemini as the sole AI engine, integrated through the official `google-genai` SDK
- Keep the codebase modular: UI, prompt logic, and API logic are cleanly separated
- Handle errors, limits, and secrets responsibly

## Features

| Feature | Description |
|---|---|
| 💬 AI Study Chat | Conversational assistant with in-session context and follow-up understanding |
| 📚 Explain Topic | Structured explanations by difficulty (Beginner/Intermediate/Advanced) and style |
| 📝 Summarizer | Short, detailed, bullet-point, or exam-revision summaries of pasted text |
| 🧠 MCQ Generator | AI-generated multiple-choice quizzes with an interactive answer-and-score flow |
| 📖 Study Notes | Structured Markdown notes (Introduction → Quick Revision) on any topic |
| 📄 Document Assistant | Upload a PDF/TXT, get a summary/notes/questions, or ask questions about it |
| 🎯 Exam Preparation | Important questions, MCQs, and a revision plan for a subject and its chapters |
| ⚙️ Settings | Choose a default AI response style (Simple, Professional, Exam-focused, etc.) |
| ℹ️ About | Project info, tech stack, and an honest note on what is/isn't implemented |

## Architecture

```
app.py  →  components/ (UI)  →  services/gemini_service.py (Gemini API)
                                       ↑
                                 utils/prompts.py (prompt templates)
                                 utils/validators.py (input checks)
                                 utils/document_processor.py (PDF/TXT handling)
                                 utils/session_manager.py (session state)
                                       ↑
                                 config/settings.py (model name, limits, options)
```

UI components never call the Gemini SDK directly — every request is routed through `services/gemini_service.py`, which owns client initialization, generation config, and error handling in one place.

## Technology Stack

- **Language:** Python 3.10+
- **App framework:** Streamlit
- **AI engine:** Google Gemini, via the official `google-genai` SDK
- **PDF processing:** pypdf
- **Config/secrets:** python-dotenv (local), Streamlit secrets (deployed)

## Project Structure

```
studygenie-ai/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── LICENSE
├── config/
│   ├── __init__.py
│   └── settings.py
├── services/
│   ├── __init__.py
│   └── gemini_service.py
├── utils/
│   ├── __init__.py
│   ├── prompts.py
│   ├── document_processor.py
│   ├── session_manager.py
│   └── validators.py
├── components/
│   ├── __init__.py
│   ├── sidebar.py
│   ├── dashboard.py
│   ├── chat.py
│   ├── topic_explainer.py
│   ├── summarizer.py
│   ├── mcq_generator.py
│   ├── notes_generator.py
│   ├── document_assistant.py
│   └── exam_prep.py
├── pages/
│   └── about.py
├── assets/
│   └── README.md
└── .streamlit/
    └── config.toml
```

## Gemini API Integration

All Gemini calls go through a single low-level wrapper, `_call_gemini()`, inside `services/gemini_service.py`. Every feature function (`generate_chat_response`, `explain_topic`, `summarize_text`, `generate_mcqs`, `generate_notes`, `analyze_document`, `answer_document_question`, `generate_exam_prep`) builds its prompt via `utils/prompts.py` and calls that wrapper, so:

- API key loading, client caching, and error classification happen in exactly one place
- The model name (`MODEL_NAME` in `config/settings.py`) can be changed once and applies everywhere
- MCQ generation asks Gemini for **strict JSON**, which is defensively parsed with a fallback extractor in case the model wraps it in code fences

## Installation

```bash
git clone <your-repo-url>
cd studygenie-ai
python -m venv .venv
```

**Activate the virtual environment:**

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Environment Variables

Copy the example file and add your key:

```bash
cp .env.example .env
```

`.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

The app loads `GEMINI_API_KEY` from the environment first, then falls back to Streamlit secrets. If neither is set, the app shows:

> "Gemini API key is not configured. Please configure GEMINI_API_KEY."

— it never crashes with a raw stack trace.

## Running Locally

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (typically `http://localhost:8501`).

## Google AI Studio API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Open the **API keys** section and create a new API key (optionally scoped to a Google Cloud project).
4. Copy the key — you won't be able to view it again in full, so store it somewhere safe.
5. Add it to your local `.env` file as `GEMINI_API_KEY=...`, or to Streamlit secrets when deploying (see below).
6. Test it by running the app locally and sending a message in **AI Study Chat**. A successful reply confirms the key works.

*(Google's exact UI labels may change over time — if a step above doesn't match what you see, look for "API key" under your Google AI Studio account/project settings.)*

## Streamlit Deployment

1. Push this repository to GitHub (see below).
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and create a new app from your repo, with `app.py` as the entry point.
3. In the app's **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
4. Deploy. The app reads this via `st.secrets["GEMINI_API_KEY"]` automatically — no code changes needed.

**Never** commit a real `.streamlit/secrets.toml` file — it's already excluded in `.gitignore`.

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Double-check `git status` shows no `.env` or `secrets.toml` staged before pushing.

## Usage

1. Launch the app and check the sidebar shows **"Gemini API: Connected."**
2. Use the sidebar to navigate between features.
3. Try **AI Study Chat** first: ask *"Explain machine learning in simple words,"* then follow up with *"Give me an example"* — the assistant retains context within the session.
4. Use **Document Assistant** to upload a PDF (e.g. lecture notes) and ask questions grounded in its content.
5. Use **MCQ Generator** to create and take a quiz, with your score shown at the end.

## Screenshots

_Add screenshots to the `assets/` folder and reference them here, e.g.:_

```markdown
![Dashboard](assets/dashboard.png)
![AI Study Chat](assets/chat.png)
```

## Security

- The Gemini API key is **never** hard-coded, logged, or displayed in the UI.
- Local development uses `.env` (via `python-dotenv`); deployment uses Streamlit secrets.
- `.gitignore` excludes `.env`, `.streamlit/secrets.toml`, `__pycache__/`, virtual environments, and temp files.
- All Gemini and document-processing errors are caught and shown as friendly messages — no raw stack traces reach the user.

## Limitations

- Document Q&A works by extracting text and passing a length-limited portion of it directly to Gemini as context — it is **not** a vector-based retrieval (RAG) system. Very long documents are truncated to a safe character budget, with a visible warning when this happens.
- Only PDF and TXT documents are supported (scanned/image-only PDFs with no extractable text are rejected with a clear message).
- Chat history, quiz state, and session statistics are session-scoped only — nothing persists after the browser session ends.
- Response quality and cost depend on the underlying Gemini model configured in `config/settings.py`.

## Future Enhancements

- Persistent chat/document history (e.g. via a lightweight database)
- True retrieval-augmented generation (RAG) for large multi-document libraries
- Export MCQs/notes to PDF, not just Markdown
- Multi-user accounts and saved study plans
- Support for additional document formats (DOCX, PPTX)

## License

Released under the [MIT License](LICENSE).
