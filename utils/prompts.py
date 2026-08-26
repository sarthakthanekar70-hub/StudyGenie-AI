"""
Prompt Engineering Templates for StudyGenie AI
"""
from typing import List, Dict, Any

SYSTEM_PERSONA = """You are StudyGenie AI, an expert academic tutor, educator, and AI learning companion.
Your goal is to provide clear, accurate, educational, and engaging explanations to help students master study concepts effectively.
Always format your output using clear GitHub-flavored Markdown headers, bullet points, code snippets, and bold text where appropriate.
"""


def apply_response_style(prompt: str, style: str) -> str:
    """Append style directives to any prompt."""
    style_directives = {
        "Simple": "Explain in simple, beginner-friendly terms with relatable analogies.",
        "Professional": "Use formal academic terminology, precise definitions, and structured breakdown.",
        "Exam-focused": "Focus on high-yield exam points, key definitions to memorize, marking scheme tips, and potential test questions.",
        "Detailed": "Provide an in-depth, thorough, comprehensive analysis with deep conceptual context.",
        "Concise": "Keep explanations bulleted, punchy, concise, and quick to read.",
        "Step-by-step": "Break down explanations into logical, sequential, step-by-step steps (Step 1, Step 2, etc.)."
    }

    directive = style_directives.get(style, style_directives["Simple"])
    return f"{prompt}\n\n[STYLE REQUIREMENT]: {directive}"


def get_chat_prompt(query: str, chat_history: List[Dict[str, str]], style: str) -> str:
    """Build conversation prompt preserving session history context."""
    history_str = ""
    if chat_history:
        history_str = "Conversation Context History:\n"
        for msg in chat_history[-10:]:
            role = "User" if msg["role"] == "user" else "StudyGenie"
            history_str += f"{role}: {msg['content']}\n"
        history_str += "\n"
    raw_prompt = f"{SYSTEM_PERSONA}\n{history_str}Current Student Question: {query}\n\nProvide a helpful, educational response considering the context history."
    return apply_response_style(raw_prompt, style)


def get_topic_explainer_prompt(topic: str, difficulty: str, explanation_style: str) -> str:
    """Prompt for structured topic explanations."""
    raw_prompt = f"""{SYSTEM_PERSONA}
Please provide a structured, comprehensive educational explanation for the topic: "{topic}".
Difficulty Target: {difficulty}
Explanation Approach: {explanation_style}
Please structure your response with the following Markdown headers:
1. **📌 Definition**: Clear concise definition of {topic}.
2. **🧠 Core Concept**: Primary principles and foundational mechanisms.
3. **⚙️ How It Works**: Step-by-step breakdown of how it operates.
4. **💡 Practical Example**: A real-world example or scenario illustrating {topic}.
5. **🌐 Real-World Applications**: Practical uses in industry, science, or daily life.
6. **🔑 Key Takeaways**: Summary bullet points for quick memory.
7. **🎯 Sample Exam Question & Answer**: A typical examination question with an ideal model answer.
"""
    return raw_prompt


def get_summarizer_prompt(text: str, summary_type: str, style: str) -> str:
    """Prompt for text summarization."""
    raw_prompt = f"""{SYSTEM_PERSONA}
Summarize the following academic study text according to the target summary type: "{summary_type}".
[TEXT TO SUMMARIZE]:
\"\"\"
{text}
\"\"\"
Requirements:
- Extract key ideas, core principles, and essential conclusions.
- Ensure structure is clean and easy to revise.
"""
    return apply_response_style(raw_prompt, style)


def get_mcq_prompt(subject: str, topic: str, num_questions: int, difficulty: str) -> str:
    """
    Prompt for generating multiple-choice questions in strict JSON array format.
    (Used directly if you call get_mcq_prompt yourself; see build_mcq_prompt
    below for the object-shaped format expected by gemini_service.py.)
    """
    return f"""{SYSTEM_PERSONA}
Generate exactly {num_questions} multiple-choice questions (MCQs) for the subject "{subject}" on the topic "{topic}".
Target Difficulty: {difficulty}.
CRITICAL: Return ONLY a valid JSON array of objects without markdown formatting codeblocks (no ```json).
Each object in the array MUST have the exact following fields:
[
  {{
    "question": "Question text here...",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "answer_index": 0,
    "explanation": "Detailed explanation of why Option A is correct and why other options are incorrect."
  }}
]
Ensure option choices are realistic and educational. The answer_index must be an integer from 0 to 3 corresponding to options[0], options[1], options[2], options[3].
Do NOT wrap output in triple backticks or any introductory text. Return raw JSON string only.
"""


def get_notes_prompt(subject: str, topic: str, level: str, length: str, style: str) -> str:
    """Prompt for comprehensive study notes generation."""
    raw_prompt = f"""{SYSTEM_PERSONA}
Create a high-quality, comprehensive set of study notes for:
- Subject: {subject}
- Topic: {topic}
- Academic Level: {level}
- Target Depth/Length: {length}
Structure the notes with clear headers:
# 📖 Study Notes: {topic}
## 1. Overview & Objectives
## 2. Fundamental Concepts & Key Terms (with bold definitions)
## 3. Detailed Technical/Conceptual Breakdown
## 4. Illustrative Examples & Formulas (if applicable)
## 5. High-Yield Exam Points & Common Misconceptions
## 6. Quick Revision Summary Sheet
"""
    return apply_response_style(raw_prompt, style)


def get_document_assistant_prompt(doc_text: str, query: str, task_type: str, style: str) -> str:
    """Prompt for document assistant tasks (Summarize, Notes, Q&A)."""
    if task_type == "summary":
        raw_prompt = f"""{SYSTEM_PERSONA}
Analyze the uploaded study document text below and generate a comprehensive summary.
[DOCUMENT CONTENT]:
\"\"\"
{doc_text}
\"\"\"
Provide key takeaways, main findings, and structured summaries of each section.
"""
    elif task_type == "notes":
        raw_prompt = f"""{SYSTEM_PERSONA}
Analyze the uploaded study document text below and generate detailed revision study notes.
[DOCUMENT CONTENT]:
\"\"\"
{doc_text}
\"\"\"
Extract core definitions, essential formulas/principles, and bulleted key points.
"""
    else:  # Q&A
        raw_prompt = f"""{SYSTEM_PERSONA}
Answer the student's question based strictly on the uploaded document text below.
If the answer cannot be determined from the document, state that clearly and provide general context.
[DOCUMENT CONTENT]:
\"\"\"
{doc_text}
\"\"\"
Student Question: {query}
"""
    return apply_response_style(raw_prompt, style)


def get_exam_prep_prompt(subject: str, topics: str, exam_type: str, difficulty: str, num_questions: int) -> str:
    """Prompt for exam preparation master guide."""
    return f"""{SYSTEM_PERSONA}
Generate a complete Exam Preparation & Strategy Guide:
- Subject: {subject}
- Coverage/Topics: {topics}
- Exam Type: {exam_type}
- Difficulty Level: {difficulty}
- Practice Question Count: {num_questions}
Structure the guide into:
1. 🎯 **Exam Strategy & High-Yield Focus Areas**
2. 📝 **Short-Answer Questions (with Model Answers & Marking Hints)**
3. 📖 **Long-Answer / Essay Questions (with Outline Answers)**
4. ⚡ **Quick Fire Revision Flashcard Concepts**
5. 📅 **Recommended 3-Step Study Plan**
"""


# ---------------------------------------------------------------------------
# Compatibility wrappers
# ---------------------------------------------------------------------------
# services/gemini_service.py calls these exact function names/signatures.
# They wrap the get_*() functions above so both naming styles work without
# needing to touch gemini_service.py.
# ---------------------------------------------------------------------------

def build_chat_prompt(history: List[Dict[str, str]], user_message: str, style: str = "Simple") -> str:
    return get_chat_prompt(user_message, history, style)


def build_topic_prompt(topic: str, difficulty: str, style: str) -> str:
    return get_topic_explainer_prompt(topic, difficulty, style)


def build_summary_prompt(text: str, summary_type: str, style: str = "Simple") -> str:
    return get_summarizer_prompt(text, summary_type, style)


def build_mcq_prompt(topic: str, count: int, difficulty: str, subject: str) -> str:
    """
    Returns the object-shaped JSON format expected by
    services.gemini_service.generate_mcqs(), i.e.
    {"questions": [{"question", "options": {A,B,C,D}, "correct_option", "explanation"}]}
    """
    return f"""{SYSTEM_PERSONA}
You are an exam question generator. Create {count} multiple-choice questions.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Requirements:
- Each question must have exactly 4 options labeled A, B, C, D.
- Exactly one option is correct.
- Include a short explanation (1-2 sentences) for the correct answer.
- Questions must be appropriate for {difficulty.lower()} level students.

Return ONLY valid JSON, with no markdown code fences and no extra commentary,
in exactly this structure:

{{
  "questions": [
    {{
      "question": "string",
      "options": {{"A": "string", "B": "string", "C": "string", "D": "string"}},
      "correct_option": "A",
      "explanation": "string"
    }}
  ]
}}
"""


def build_notes_prompt(subject: str, topic: str, level: str, length: str, style: str = "Simple") -> str:
    return get_notes_prompt(subject, topic, level, length, style)


def build_document_summary_prompt(document_text: str, mode: str, style: str = "Simple") -> str:
    return get_document_assistant_prompt(document_text, "", mode, style)


def build_document_qa_prompt(document_text: str, question: str, style: str = "Simple") -> str:
    return get_document_assistant_prompt(document_text, question, "qa", style)


def build_exam_prep_prompt(subject: str, chapters: str, exam_type: str,
                            difficulty: str, num_questions: int) -> str:
    return get_exam_prep_prompt(subject, chapters, exam_type, difficulty, num_questions)