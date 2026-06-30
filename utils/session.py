import streamlit as st

def init_session():

    defaults = {
        "score": 0,
        "q_index": 0,
        "questions": [],
        "started": False,
        "subject": "",
        "attempted": 0,
        "skipped_questions": [],
        "total_questions": 0,
        "revisited_skips": False,
        "target_questions": 5,
        "skipped_count": 0,
        "saved": False,
        "name": "",
        "force_submit": False,
        "wrong_topics": [],
        "wrong_answers": 0,
        "ai_tutor": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value