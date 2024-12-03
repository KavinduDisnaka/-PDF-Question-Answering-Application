import streamlit as st
import requests

# Title
st.title("PDF Question-Answering Application")

# File upload widget
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# Input for questions
question = st.text_input("Ask a question")

# Upload PDF
if uploaded_file is not None:
    files = {"file": ("document.pdf", uploaded_file.getvalue())}
    response = requests.post("http://127.0.0.1:8002/upload/", files=files)

    if response.status_code == 200:
        st.success(response.json().get("message", "File uploaded successfully!"))
    else:
        st.error(f"Failed to upload and process the PDF: {response.text}")

# Ask a question
if question:
    if st.button("Ask"):
        # Ensure the question is sent as a JSON payload
        response = requests.post("http://127.0.0.1:8002/ask/", json={"question": question})

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found.")
            st.write(f"**Answer:** {answer}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
