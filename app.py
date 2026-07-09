import streamlit as st
from utils.session import init_session

st.set_page_config(
    page_title="AI Learning Companion",
    page_icon="🤖",
    layout="wide"
)

init_session()

st.switch_page("pages/home.py")