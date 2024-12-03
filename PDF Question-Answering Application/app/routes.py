from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.model import process_text, get_answer
from app.pdf_processing import extract_text_from_pdf

router = APIRouter()

# Define a Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Process the PDF and extract text
        pdf_text = extract_text_from_pdf(file.file)
        chunks_processed = process_text(pdf_text)
        return {"message": "PDF processed successfully", "chunks_processed": chunks_processed}
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}

@router.post("/ask/")
async def ask_question(request: QuestionRequest):
    try:
        question = request.question  # Get the question from the request body
        answer = get_answer(question)
        return {"answer": answer}
    except Exception as e:
        return {"error": f"Failed to fetch answer: {str(e)}"}
