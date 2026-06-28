import streamlit as st
import random
import time
from database import conn, cursor
from questions import python_questions, ai_questions, ml_questions
from pdf_generator import generate_pdf

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
if "score" not in st.session_state:
    st.session_state.score = 0

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "started" not in st.session_state:
    st.session_state.started = False

if "subject" not in st.session_state:
    st.session_state.subject = ""

if "attempted" not in st.session_state:
    st.session_state.attempted = 0

if "skipped_questions" not in st.session_state:
    st.session_state.skipped_questions = []

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "revisited_skips" not in st.session_state:
    st.session_state.revisited_skips = False

if "target_questions" not in st.session_state:
    st.session_state.target_questions = 5

if "skipped_count" not in st.session_state:
    st.session_state.skipped_count = 0

if "saved" not in st.session_state:
    st.session_state.saved = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "force_submit" not in st.session_state:
    st.session_state.force_submit = False

if "wrong_topics" not in st.session_state:
    st.session_state.wrong_topics = []

if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = 0

if "ai_tutor" not in st.session_state:
    st.session_state.ai_tutor = True


# ---------------- UI ----------------
st.markdown("## 🤖 AI Learning Companion")
st.caption("Learn • Practice • Improve")

st.subheader("👤 Student Details")

name = st.text_input("Enter your Name")

subject = st.selectbox(
    "Choose Subject",
    ["Python", "AI Basics", "Machine Learning"]
)

st.session_state.ai_tutor = st.checkbox(
    "🤖 AI Tutor Mode (Explain answers)",
    value=True
)

# ---------------- START QUIZ ----------------
if st.button("Start Quiz") and name:
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

        accuracy = (
            correct_answers /
        st.session_state.attempted * 100
        ) if st.session_state.attempted > 0 else 0

        if accuracy >= 80:
            grade = "A"
        elif accuracy >= 60:
            grade = "B"
        elif accuracy >= 40:
            grade = "C"
        else:
            grade = "Needs Improvement"

        st.subheader("📊 Performance Report")

        st.write("👤 Student:", st.session_state.name)
        st.write("📚 Subject:", st.session_state.subject)
        st.write("🎯 Accuracy:", f"{accuracy:.2f}%")
        st.write("🎓 Grade:", grade)

        st.subheader("📊 Analytics Dashboard")

        st.write("✅ Correct Answers:", correct_answers)
        st.write("❌ Wrong Answers:", wrong_answers)
        st.write("⏭️ Skipped Questions:", st.session_state.skipped_count)

        chart_data = {
                "Correct": correct_answers,
                "Wrong": wrong_answers,
                "Skipped": st.session_state.skipped_count
                        }

        st.bar_chart(chart_data)
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
                            st.info(f"""
                    🧠 AI Tutor Explanation:

                    ✔ Correct Answer: {q['answer']}

                    💡 Why: {q['explanation']}

                    🎯 Tip: Revise {q['topic']} once for strong exam prep.
                    """)

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