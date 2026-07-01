import streamlit as st

st.title("📝 Quiz")

if not st.session_state.started:
    st.warning("⚠️ Please start the quiz from the Home page.")
    st.stop()

st.success("Quiz page connected successfully!")

st.write("Name:", st.session_state.name)
st.write("Subject:", st.session_state.subject)
st.write("Questions Loaded:", len(st.session_state.questions))