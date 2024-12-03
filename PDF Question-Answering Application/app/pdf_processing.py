from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Extract text or add an empty string
        if not text.strip():
            raise ValueError("No text found in the PDF")
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")
