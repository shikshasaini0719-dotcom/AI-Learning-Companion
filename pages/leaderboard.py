import streamlit as st
from database import cursor

st.title("🏆 Leaderboard")
cursor.execute("""
SELECT name, subject, score, attempted ,timestamp
FROM results
ORDER BY score DESC, attempted DESC, timestamp DESC
LIMIT 10
""")

rows = cursor.fetchall()

if rows:

    table = []

    rank = 1

    for name, subject, score, attempted , timestamp in rows:

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
            "Subject": subject,
            "Score": score,
            "Attempted": attempted
            "Date & Time": timestamp.replace("T", " ")
        })

        rank += 1

    st.dataframe(table, use_container_width=True)

else:
    st.info("No quiz attempts found yet.")
