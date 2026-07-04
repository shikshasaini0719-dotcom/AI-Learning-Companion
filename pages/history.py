import streamlit as st
from database import cursor
from datetime import datetime

st.title("📜 Quiz History")

cursor.execute("""
SELECT name, subject, score, attempted, timestamp
FROM results
ORDER BY timestamp DESC
""")

rows = cursor.fetchall()

if rows:
    st.metric("Total Attempts", len(rows))
    average = sum(score for _, _, score, _, _ in rows) / len(rows)

    st.metric("Average Score", f"{average:.1f}")
    table = []

    for name, subject, score, attempted, timestamp in rows:
        formatted_time = datetime.fromisoformat(timestamp).strftime(
            "%d %b %Y %I:%M %p"
        )

        table.append({
            "Name": name,
            "Subject": subject,
            "Score": f"{score}/{attempted}",
            "Date & Time": formatted_time
        })

    st.dataframe(table, use_container_width=True)

else:
    st.info("No quiz attempts yet. Complete a quiz to see your history.")