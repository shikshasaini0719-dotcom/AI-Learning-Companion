import streamlit as st
from database import cursor
from datetime import datetime

st.title("📜 Quiz History")
st.caption("View all your previous quiz attempts and track your progress.")

cursor.execute("""
SELECT name, subject, score, attempted, timestamp
FROM results
ORDER BY timestamp DESC
""")

rows = cursor.fetchall()

if rows:

    average = sum(score for _, _, score, _, _ in rows) / len(rows)
    best_score = max(score for _, _, score, _, _ in rows)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📝 Total Attempts", len(rows))

    with col2:
        st.metric("⭐ Average Score", f"{average:.1f}")

    with col3:
        st.metric("🏆 Best Score", best_score)

    st.divider()
    table = []

    for name, subject, score, attempted, timestamp in rows:
        formatted_time = datetime.fromisoformat(timestamp).strftime(
            "%d %b %Y %I:%M %p"
        )
        accuracy = round((score / attempted) * 100) if attempted else 0

        table.append({
            "Name": name,
            "Subject": subject,
            "Score": f"{score}/{attempted}",
            "Accuracy": f"{accuracy}%",
            "Date & Time": formatted_time
        })

    st.dataframe(table, use_container_width=True)

else:
    st.info("No quiz attempts yet. Complete a quiz to see your history.")