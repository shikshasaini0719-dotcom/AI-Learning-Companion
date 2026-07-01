import streamlit as st


def home_page():

    st.title("🤖 AI Learning Companion")

    st.markdown("""
### Learn • Practice • Improve

Welcome to your personalized AI-powered learning platform.
""")

    st.divider()

    st.subheader("📖 About This Project")

    st.write("""
AI Learning Companion is an interactive quiz platform developed using Python and Streamlit.

It helps students:

✅ Practice MCQs

✅ Learn from AI explanations

✅ Track their performance

✅ View leaderboard

✅ Download PDF reports

✅ Improve weak topics
""")

    st.subheader("🛠 Technologies Used")

    col1, col2 = st.columns(2)

    with col1:
        st.success("🐍 Python")
        st.success("🌐 Streamlit")
        st.success("🗄 SQLite")

    with col2:
        st.success("📄 ReportLab")
        st.success("📊 Matplotlib")
        st.success("🤖 AI Tutor")