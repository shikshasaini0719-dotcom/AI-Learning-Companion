import streamlit as st
from database import cursor
from datetime import datetime

st.title("🏆 Leaderboard")
st.caption(
    "Top performers based on their best quiz scores."
)

st.divider()
cursor.execute("""
SELECT
    name,
    subject,
    MAX(score) AS best_score,
    MAX(attempted) AS attempted,
    MAX(timestamp) AS timestamp
FROM results
GROUP BY name, subject
ORDER BY best_score DESC, attempted DESC
LIMIT 10
""")

rows = cursor.fetchall()

if rows:
    total_players = len(rows)
    highest_score = max(score for _, _, score, _, _ in rows)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("👥 Players", total_players)

    with col2:
        st.metric("🏆 Highest Score", highest_score)

    st.divider()

    table = []

    rank = 1

    for name, subject, score, attempted , timestamp in rows:
        formatted_time = datetime.fromisoformat(timestamp).strftime(
            "%d %b %Y %I:%M %p"
        )
        accuracy = round((score / attempted) * 100) if attempted else 0

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
            "Accuracy": f"{accuracy}%",
            "Attempted": attempted,
            "Date & Time": formatted_time
        })

        rank += 1

    st.dataframe(table, use_container_width=True)

else:
    st.info("No quiz attempts found yet.")
