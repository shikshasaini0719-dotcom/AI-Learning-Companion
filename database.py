import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect("quiz.db", check_same_thread=False)

cursor = conn.cursor()

# Create table
current_time = datetime.now().strftime("%d %b %Y %I:%M %p")
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    score INTEGER,
    attempted INTEGER,
    timestamp TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER
)
""")

conn.commit()
