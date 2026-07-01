import streamlit as st
import random
import time
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
from utils.session import init_session

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

    # sort by score (highest first)
    data.sort(key=lambda x: x[1], reverse=True)

    return data

# ---------------- SESSION STATE ----------------
init_session()

# ---------------- UI ----------------


    
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

# Exam completed
    if (
    st.session_state.attempted >= st.session_state.target_questions
    or st.session_state.force_submit
):

        if st.session_state.skipped_count > 0:
            st.warning(
            f"⚠️ Exam submitted with {st.session_state.skipped_count} skipped question(s)."
        )

        if not st.session_state.saved:

            try:
                with open("students.txt", "a") as f:
                    f.write(st.session_state.name + "\n")

                cursor.execute(
                    """
                    INSERT INTO results(name, subject, score, attempted)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        st.session_state.name,
                        st.session_state.subject,
                        st.session_state.score,
                        st.session_state.attempted,
                    ),
                )

                conn.commit()

                st.session_state.saved = True

            except Exception as e:
                st.error(f"Error saving data: {e}")
                st.session_state.saved = True

        st.balloons()
        st.success("🎉 Exam Completed!")

        st.markdown(
            f"## 🏆 Final Score: {st.session_state.score}/{st.session_state.target_questions}"
    )

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
        st.subheader("🏆 Leaderboard")

        data = load_leaderboard()

        if data:
            rank = 1
            table = []

            for name, score in data:
                medal = ""

                if rank == 1:
                    medal = "🥇"
                elif rank == 2:
                    medal = "🥈"
                elif rank == 3:
                    medal = "🥉"

                table.append({
                    "Rank": f"{medal} {rank}",
                    "Name": name,
                    "Score": score
                })

                rank += 1

            st.dataframe(table)
        else:
            st.info("No leaderboard data yet.")
        st.subheader("📚 Topics To Review")

        if st.session_state.wrong_topics:

            for topic in  set(st.session_state.wrong_topics):
                st.write("🔹", topic)

        else:
            st.success("🎉 Excellent! No weak topics found.")

        attempts = 0

        cursor.execute(
            "SELECT COUNT(*) FROM results WHERE name = ?",
            (st.session_state.name,)
        )

        attempts = cursor.fetchone()[0]


        st.write("🔄 Previous Attempts:", attempts)
        # Generate PDF
        pdf_file = generate_pdf(
            st.session_state.name,
            st.session_state.subject,
            st.session_state.score,
            st.session_state.target_questions,
            accuracy,
            grade,
            st.session_state.wrong_topics
        )

# Download Button
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📥 Download PDF Report",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
        )
        if st.button("🔄 Restart Exam"):

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
            
            st.rerun()  
    else:

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
                        

    
#-------DISPLAY ----------------
if st.session_state.started:
    st.write(f"⭐ Score: {st.session_state.score}")

st.write(
    f"📊 Progress: {st.session_state.attempted}/{st.session_state.target_questions}"
)