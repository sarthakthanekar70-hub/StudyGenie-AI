"""
app.py

StudyGenie AI — main application entry point.

Responsibilities:
- Configure the Streamlit page
- Initialize session state
- Render the sidebar and get the selected page
- Route to the correct feature component
- Handle application-level errors gracefully

No business logic (Gemini calls, prompt building, validation) lives here —
that belongs in services/, utils/, and components/.
"""
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE, RESPONSE_STYLES
from utils.session_manager import init_session_state
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.chat import render_chat
from components.topic_explainer import render_topic_explainer
from components.summarizer import render_summarizer
from components.mcq_generator import render_mcq_generator
from components.notes_generator import render_notes_generator
from components.document_assistant import render_document_assistant
from components.exam_prep import render_exam_prep
from pages.about import render_about


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Minimal, restrained custom CSS — improves polish without over-engineering
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Tighten default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Feature / stat cards get a subtle shadow */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
    }

    /* Sidebar radio nav: a bit more breathing room between items */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 4px 0;
    }

    /* Metric labels slightly muted */
    div[data-testid="stMetricLabel"] {
        opacity: 0.75;
    }

    /* Buttons: slightly rounder */
    button[kind="primary"], button[kind="secondary"] {
        border-radius: 8px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
init_session_state()


# ---------------------------------------------------------------------------
# Settings page (small enough to keep inline rather than its own file)
# ---------------------------------------------------------------------------
def render_settings() -> None:
    st.title("⚙️ Settings")
    st.caption("Preferences that apply across StudyGenie AI features.")

    current_style = st.session_state.get("response_style", "Simple")
    new_style = st.selectbox(
        "Default AI response style",
        RESPONSE_STYLES,
        index=RESPONSE_STYLES.index(current_style) if current_style in RESPONSE_STYLES else 0,
        help="Used by AI Study Chat to shape tone and depth of responses.",
    )
    st.session_state["response_style"] = new_style

    st.divider()
    st.caption(
        "The Gemini API key is configured via the GEMINI_API_KEY environment "
        "variable or Streamlit secrets — it is never entered or displayed here."
    )


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------
PAGE_ROUTES = {
    "🏠 Dashboard": render_dashboard,
    "💬 AI Study Chat": render_chat,
    "📚 Explain Topic": render_topic_explainer,
    "📝 Summarizer": render_summarizer,
    "🧠 MCQ Generator": render_mcq_generator,
    "📖 Study Notes": render_notes_generator,
    "📄 Document Assistant": render_document_assistant,
    "🎯 Exam Preparation": render_exam_prep,
    "⚙️ Settings": render_settings,
    "ℹ️ About": render_about,
}


def main() -> None:
    selected_page = render_sidebar()
    st.session_state["current_page"] = selected_page

    render_fn = PAGE_ROUTES.get(selected_page)
    if render_fn is None:
        st.error("Unknown page selected.")
        return

    try:
        render_fn()
    except Exception as exc:  # noqa: BLE001 - last-resort safety net for the whole app
        st.error(
            "Something unexpected went wrong while loading this page. "
            "Please try again or switch pages."
        )
        with st.expander("Technical details (for debugging)"):
            st.code(str(exc))


if __name__ == "__main__":
    main()
