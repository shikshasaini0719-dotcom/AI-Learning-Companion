import streamlit as st

from datetime import datetime
from utils.session import init_session
from database import conn, cursor
from utils.analytics import (
    calculate_accuracy,
    calculate_grade,
    show_performance_report,
    show_analytics_dashboard,
)
from pdf_generator import generate_pdf


init_session()

st.title("🎉 Quiz Results")

# Save result only once
if not st.session_state.saved:
    current_time = datetime.now().isoformat(sep=" ", timespec="seconds")

    try:
        with open("students.txt", "a") as f:
            f.write(st.session_state.name + "\n")

        cursor.execute(
            """
            INSERT INTO results(name, subject, score, attempted , timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                st.session_state.name,
                st.session_state.subject,
                st.session_state.score,
                st.session_state.attempted,
                current_time
            ),
        )

        conn.commit()

        st.session_state.saved = True

    except Exception as e:
        st.error(f"Error saving data: {e}")
        st.session_state.saved = True

st.success("🎉 Quiz Completed!")

st.metric("Score", st.session_state.score)
st.metric("Attempted", st.session_state.attempted)
st.metric("Skipped", st.session_state.skipped_count)

correct_answers = st.session_state.score
wrong_answers = st.session_state.wrong_answers

accuracy = calculate_accuracy(
    correct_answers,
    st.session_state.attempted
)

grade = calculate_grade(accuracy)

show_performance_report(
    st.session_state.name,
    st.session_state.subject,
    accuracy,
    grade
)

show_analytics_dashboard(
    correct_answers,
    wrong_answers,
    st.session_state.skipped_count
)

st.subheader("📚 Topics To Review")

if st.session_state.wrong_topics:

    for topic in set(st.session_state.wrong_topics):
        st.write("🔹", topic)

else:
    st.success("🎉 Excellent! No weak topics found.")

pdf_file = generate_pdf(
    st.session_state.name,
    st.session_state.subject,
    st.session_state.score,
    st.session_state.target_questions,
    accuracy,
    grade,
    st.session_state.wrong_topics
)

with open(pdf_file, "rb") as file:
    st.download_button(
        label="📥 Download PDF Report",
        data=file,
        file_name=pdf_file,
        mime="application/pdf"
    )

if st.button("🔄 Restart Exam", use_container_width=True):

    st.session_state.started = False
    st.session_state.saved = False
    st.session_state.questions = []
    st.session_state.total_questions = 0
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.attempted = 0
    st.session_state.skipped_questions = []
    st.session_state.skipped_count = 0
    st.session_state.wrong_topics = []
    st.session_state.name = ""
    st.session_state.subject = ""
    st.session_state.force_submit = False
    st.session_state.wrong_answers = 0

    st.switch_page("pages/home.py")