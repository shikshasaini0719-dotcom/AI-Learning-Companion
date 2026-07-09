import streamlit as st
import random

from questions import python_questions, ai_questions, ml_questions
from utils.session import init_session

init_session()

st.title("🤖 AI Learning Companion")

st.caption("Learn • Practice • Improve • Analyze")

st.markdown("---")

st.markdown(
    """
## 👋 Welcome!

Master **Python**, **Artificial Intelligence**, and **Machine Learning**
through interactive quizzes with instant feedback and performance analytics.

Choose a subject below and begin your learning journey!
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### 📚 Learn

Practice subject-wise quizzes
with curated questions.
"""
    )

with col2:
    st.success(
        """
### 📊 Analyze

Track your accuracy,
grades and performance.
"""
    )

with col3:
    st.warning(
        """
### 🏆 Improve

Review weak topics
and download PDF reports.
"""
    )

st.divider()

st.subheader("🎓 Student Information")

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

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📚 Subjects", 3)

with col2:
    st.metric("🎯 Questions", len(python_questions)+len(ai_questions)+len(ml_questions))

with col3:
    st.metric("🤖 AI Tutor", "ON")

# ---------------- START QUIZ ----------------
start = st.button(
"🚀 Start Learning",
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

st.markdown("---")

st.caption(
    "© 2026 AI Learning Companion | Built with ❤️ using Streamlit"
)