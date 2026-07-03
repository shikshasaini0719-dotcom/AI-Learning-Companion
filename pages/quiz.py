import streamlit as st
import time

from utils.session import init_session
init_session()

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
    if (
    st.session_state.attempted >= st.session_state.target_questions
    or st.session_state.force_submit
):
        st.switch_page("pages/results.py")
        st.stop()
        
    if q_index < len(questions):

        q = questions[q_index]

        st.markdown("### 🧾 Question")
        st.success(q["question"])

        answer = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"ans_{q_index}"
        )

        col1, col2 = st.columns(2)

        with col1:
            submit = st.button("✅ Submit Answer")

        with col2:
            skip = st.button("⏭️ Skip")

        if st.button("💡 Hint"):
            st.warning(f"Hint: This question is about {q['topic']}")

        if submit:

            if answer == q["answer"]:
                st.success("🎉 Correct!")

                if st.session_state.ai_tutor:
                    show_ai_tutor(q)

                st.session_state.score += 1

            else:
                st.error(f"❌ Wrong! Correct answer: {q['answer']}")

                st.session_state.wrong_answers += 1

                if q["topic"] not in st.session_state.wrong_topics:
                    st.session_state.wrong_topics.append(q["topic"])

                if st.session_state.ai_tutor:
                    st.info(f"""
        🧠 AI Tutor Explanation:

        ✔ Correct Answer: {q['answer']}

        💡 Explanation: {q['explanation']}

        ⚠️ Common Mistake: Students often confuse this topic.

        🎯 Tip: Focus on {q['topic']} for improvement.
        """)

            st.session_state.attempted += 1

            time.sleep(4)

            st.session_state.q_index += 1

            st.rerun()

        if skip:

            st.session_state.skipped_count += 1

            st.session_state.skipped_questions.append(
            questions[q_index]
            )

            st.session_state.q_index += 1

            st.rerun()

    else:

        remaining = (
        st.session_state.target_questions
        - st.session_state.attempted
        )

        st.warning(
            f"⚠️ Question bank exhausted. "
            f"You still need {remaining} more answered question(s)."
        )

        if (
            st.session_state.skipped_questions
            and not st.session_state.revisited_skips
        ):

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Continue With Skipped Questions"):

                    st.session_state.questions = (
                    st.session_state.skipped_questions.copy()
                    )

                    st.session_state.skipped_questions = []
                    st.session_state.q_index = 0
                    st.session_state.revisited_skips = True

                    st.rerun()

            with col2:
                if st.button("✅ Submit Exam Anyway"):

                    st.session_state.force_submit = True

                    st.rerun()