import streamlit as st

st.title("ℹ️ About AI Learning Companion")

st.markdown("""
## 🎯 Project Overview

AI Learning Companion is an interactive quiz platform developed using **Python** and **Streamlit**.

It helps students strengthen their understanding of **Python**, **Artificial Intelligence**, and **Machine Learning** through quizzes, AI explanations, performance analytics, and downloadable reports.
""")

st.divider()

st.subheader("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Interactive MCQ Quiz")
    st.success("🤖 AI Tutor")
    st.success("📊 Performance Analytics")
    st.success("📄 PDF Report")

with col2:
    st.success("🏆 Leaderboard")
    st.success("📜 Quiz History")
    st.success("💡 Hints & Explanations")
    st.success("🗄 SQLite Database")

st.divider()

st.subheader("🛠 Tech Stack")

col1, col2 = st.columns(2)

with col1:
    st.info("🐍 Python")
    st.info("🌐 Streamlit")
    st.info("🗄 SQLite")

with col2:
    st.info("📄 ReportLab")
    st.info("📊 Matplotlib")
    st.info("🐙 Git & GitHub")

st.divider()

st.subheader("🎓 Skills Demonstrated")

st.markdown("""
- Python Programming
- Streamlit Application Development
- SQLite Database Integration
- Session State Management
- Data Analytics & Visualization
- PDF Report Generation
- Git & GitHub Version Control
""")

st.divider()

st.subheader("📂 Project Structure")

st.code("""
AI-Learning-Companion/
│
├── app.py
├── database.py
├── questions.py
├── pdf_generator.py
│
├── pages/
│   ├── home.py
│   ├── quiz.py
│   ├── results.py
│   ├── history.py
│   ├── leaderboard.py
│   └── about.py
│
├── utils/
│   ├── session.py
│   ├── analytics.py
│   └── ai_tutor.py
""")

st.divider()

st.subheader("🚀 Future Enhancements")

st.write("""
- AI-generated quiz questions
- Adaptive difficulty levels
- User login system
- Cloud database integration
- Performance prediction using Machine Learning
""")

st.divider()

st.caption("Built with Python • Streamlit • SQLite • ReportLab")

st.divider()

st.subheader("👩‍💻 Developer")

st.info("""
**Shiksha Saini**

B.Tech CSE (Artificial Intelligence & Machine Learning)

AI Learning Companion Version 1.0
""")