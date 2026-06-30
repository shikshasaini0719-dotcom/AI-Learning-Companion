import streamlit as st


def show_ai_tutor(question):
    st.info(f"""
🧠 AI Tutor Explanation:

✔ Correct Answer: {question['answer']}

💡 Explanation: {question['explanation']}

⚠ Common Mistake:
Students often confuse this topic.

🎯 Tip:
Focus on {question['topic']} for improvement.
""")