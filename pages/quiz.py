import streamlit as st
import time

from database import conn, cursor
from pdf_generator import generate_pdf
from utils.ai_tutor import show_ai_tutor
from utils.analytics import (
    calculate_accuracy,
    calculate_grade,
    show_performance_report,
    show_analytics_dashboard,
)

def load_leaderboard():
    data = []

    try:
        with open("leaderboard.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")

                if len(parts) == 2:
                    name = parts[0]
                    score = int(parts[1])
                    data.append((name, score))
    except:
        pass

    data.sort(key=lambda x: x[1], reverse=True)
    return data


st.title("📝 Quiz")

if not st.session_state.started:
    st.warning("⚠️ Please start the quiz from the Home page.")
    st.stop()


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