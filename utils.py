# utils.py
import sqlite3
import PyPDF2
from pdf2image import convert_from_bytes
import pdfplumber
import pytesseract
from PIL import Image
import io
import datetime

# SQLite DB Setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Validate user login
def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text() or ""
    except Exception as e:
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            return None
    return text

# Extract text from image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Convert PDF to images
def convert_pdf_to_images(pdf_file):
    try:
        images = convert_from_bytes(pdf_file.read())
        return images
    except Exception as e:
        return []

# Apply theme function
def apply_theme():
    if st.session_state.theme == "Light":
        st.markdown("""
            <style>
            .stApp {
                background-color: #FFE0B2;  /* Light orange background */
                color: #333333;  /* Dark gray text */
            }
            h1, h2, h3, h4, h5, h6 {
                color: #FF9800;  /* Orange headers */
            }
            .stButton>button {
                background-color: #FF9800;  /* Orange buttons */
                color: white;
                border: none;
            }
            .stButton>button:hover {
                background-color: #F57C00;  /* Darker orange on hover */
            }
            .stSuccess {
                color: #4CAF50;  /* Green for success messages */
            }
            [data-testid="stSidebar"] {
                background-color: #FF9800;  /* Orange sidebar */
            }
            </style>
        """, unsafe_allow_html=True)
    elif st.session_state.theme == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #1e1e1e;  /* Dark gray background */
                color: #ffffff;  /* White text */
            }
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff;  /* Purple headers */
            }
            .stButton>button {
                background-color: #bb86fc;  /* Purple buttons */
                color: #ffffff;  /* Black text on buttons */
                border: none;
            }
            .stButton>button:hover {
                background-color: #9a67ea;  /* Darker purple on hover */
            }
            .stSuccess {
                color: #03dac6;  /* Teal for success messages */
            }
            [data-testid="stSidebar"] {
                background-color: #333333;  /* Darker gray sidebar */
                color: #BB86FC;  /* Purple text in sidebar (matching headers/buttons) */
            }
            [data-testid="stSidebar"] a {
                color: #BB86FC;  /* Purple color for page links in sidebar */
            }
            [data-testid="stSidebar"] a:hover {
                color: #ffffff;  /* Light gray on hover for page links */
            }
            </style>
        """, unsafe_allow_html=True)
