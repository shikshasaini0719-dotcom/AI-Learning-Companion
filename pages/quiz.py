import streamlit as st
import random
import time

from utils.session import init_session

init_session()  

from database import conn, cursor
from questions import python_questions, ai_questions, ml_questions
from pdf_generator import generate_pdf
from utils.ai_tutor import show_ai_tutor
from utils.analytics import (
    calculate_accuracy,
    calculate_grade,
    show_performance_report,
    show_analytics_dashboard,
)

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

st.write("Button:", start)
st.write("Name:", name)

if start and name:
    st.write("Started:", st.session_state.started)
    st.write("Questions Loaded:", len(st.session_state.questions))
    st.write("Subject:", st.session_state.subject)
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

    st.write("Loaded Questions:", len(st.session_state.questions))

    random.shuffle(st.session_state.questions)

    st.session_state.total_questions = st.session_state.target_questions
    
    st.write("Started:", st.session_state.started)
    st.write("Subject:", st.session_state.subject)
    st.write("Questions:", len(st.session_state.questions))
# ---------------- QUIZ LOGIC ----------------
if st.session_state.started and st.session_state.questions:

    q_index = st.session_state.q_index
    questions = st.session_state.questions

    # Progress
    if st.session_state.target_questions > 0:
        progress = min(
            st.session_state.attempted /
            st.session_state.target_questions,
            1.0
        )
    else:
        progress = 0

    st.progress(progress)

    st.info(
        f"""
📚 Total Questions Available: {len(st.session_state.questions)}

🎯 Questions Required: {st.session_state.target_questions}

✅ Attempted: {st.session_state.attempted}

⏭️ Skipped: {st.session_state.skipped_count}

🎯 Questions Left To Solve:
{st.session_state.target_questions - st.session_state.attempted}
"""
    )