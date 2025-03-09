# app.py
import streamlit as st
from utils import init_db

# Initialize the database
init_db()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'reports' not in st.session_state:
    st.session_state.reports = []

# # Set page config for the main page
st.set_page_config(page_title="SYNAPSE", page_icon="🏠", layout="wide")

st.sidebar.title("SYNAPSE")
st.sidebar.write(f"Logged in: {st.session_state.logged_in}")  # Debug output
st.write("Welcome to SYNAPSE! Navigate using the sidebar.")