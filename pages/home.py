import streamlit as st
import random

from questions import python_questions, ai_questions, ml_questions
from utils.session import init_session

init_session()

st.title("🤖 AI Learning Companion")

st.markdown("""
### Learn • Practice • Improve

Welcome to your personalized AI-powered learning platform.
""")

st.divider()

st.subheader("👤 Student Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Enter Your Name")

with col2:
    subject = st.selectbox(
    "📚 Choose Subject",
    ["Python", "AI Basics", "Machine Learning"]
    )

st.session_state.ai_tutor = st.checkbox(
    "🤖 AI Tutor Mode (Explain answers)",
    value=True
)

# ---------------- START QUIZ ----------------
start = st.button(
"🚀 Start Quiz",
use_container_width=True
)

if start and name:
    st.session_state.started = True
    st.session_state.saved = False
    st.session_state.name = name
    st.session_state.score = 0
    st.session_state.q_index = 0
    st.session_state.attempted = 0
    st.session_state.skipped_count = 0
    st.session_state.skipped_questions = []
    st.session_state.wrong_topics = []
    st.session_state.revisited_skips = False
    st.session_state.force_submit = False
    st.session_state.wrong_answers = 0
    st.session_state.subject = subject
    if subject == "Python":
        st.session_state.questions = python_questions.copy()

    elif subject == "AI Basics":
        st.session_state.questions = ai_questions.copy()

    else:
        st.session_state.questions = ml_questions.copy()

    random.shuffle(st.session_state.questions)

    st.session_state.total_questions = st.session_state.target_questions
    st.switch_page("pages/quiz.py")