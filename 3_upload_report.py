# pages/3_Upload_Report.py
import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_image, convert_pdf_to_images
import io
import datetime
from PIL import Image

# Set page config
st.set_page_config(page_title="Upload Report", page_icon="📤")

def main():
    # Debug output in sidebar
    st.sidebar.write(f"Logged in: {st.session_state.logged_in}")
    st.sidebar.write(f"Username: {st.session_state.username}")

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()  # Stop execution if not logged in
    else:
        # st.title("Upload Diagnostic Report")

        col1, col2 = st.columns([5, 1])  # 4:1 ratio to push button to the right
        with col1:
            st.title("Upload Diagnostic Report")
            
        with col2:
            
            st.page_link("pages/4_uploaded_reports.py", label="Uploaded Reports", icon="🔒")  # Links to Login page


        st.write(f"Welcome, {st.session_state.username}!")  # Confirm user

        uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

        if uploaded_file:
            file_type = uploaded_file.type
            extracted_text = ""
            images = []

            if file_type == "application/pdf":
                st.info("Processing PDF file...")
                images = convert_pdf_to_images(uploaded_file)
                uploaded_file.seek(0)
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_type.startswith("image/"):
                st.info("Processing Image file...")
                image = Image.open(uploaded_file)
                extracted_text = extract_text_from_image(image)
                images = [image]

            col1, col2 = st.columns(2)
            with col1:
                st.header("Report Preview")
                if images:
                    for img in images:
                        st.image(img, caption="Page Preview", use_container_width=True)
                else:
                    st.warning("No preview available.")
            with col2:
                st.header("Extracted Text")
                if extracted_text:
                    st.text_area("  ", extracted_text, height=460)
                else:
                    st.warning("No text extracted.")

            upload_time = datetime.datetime.now()
            file_bytes = io.BytesIO(uploaded_file.getvalue())
            file_size = file_bytes.getbuffer().nbytes

            st.session_state.reports.append({
                "name": uploaded_file.name,
                "file": file_bytes,
                "upload_time": upload_time,
                "type": file_type,
                "size": file_size
            })

if __name__ == "__main__":
    main()