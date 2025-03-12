# app.py
import streamlit as st
from utils import init_db
import base64

# Initialize the database
init_db()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'subscribed' not in st.session_state:
    st.session_state.subscribed = False  # Default to free tier (not subscribed)

# Set page config for the main page
st.set_page_config(page_title="SYNAPSE", page_icon="🏠", layout="wide")

# Sidebar navigation (Streamlit auto-generates this from page files)
st.sidebar.title("SYNAPSE")
st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
if st.session_state.logged_in and st.session_state.username:
    st.sidebar.write(f"Username: {st.session_state.username}")
    st.sidebar.write(f"Subscribed: {'Yes' if st.session_state.subscribed else 'No'}")  # Show subscription status

# Welcome message (optional, only if no page is loaded)
st.title("Welcome to SYNAPSE!") 


# st.write("Navigate using the sidebar or page links.")

col1, col2 = st.columns([5, 1])  # 4:1 ratio to push button to the right
with col1:
    st.write("👈 Navigate using the sidebar or page links 👉")
with col2:
    page_link = st.page_link("pages/1_home.py",icon = "🏠")

st.image("landing_page.jpg")
