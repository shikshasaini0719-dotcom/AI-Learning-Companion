import streamlit as st

from utils.session import init_session
from database import conn, cursor

init_session()

st.title("🎉 Quiz Results")

# Save result only once
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

st.success("🎉 Quiz Completed!")

st.metric("Score", st.session_state.score)
st.metric("Attempted", st.session_state.attempted)
st.metric("Skipped", st.session_state.skipped_count)