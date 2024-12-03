import os
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# Initialize OpenAI
llm = OpenAI(api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Global variable to track current document
current_document = None


def process_text(raw_text):
    global current_document
    try:
        # Split the text into chunks
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(raw_text)

        # Create documents
        documents = [
            Document(page_content=text, metadata={"source": f"chunk_{i}"})
            for i, text in enumerate(texts)
        ]

        # Store the documents globally
        current_document = documents

        return len(texts)
    except Exception as e:
        print(f"Error in process_text: {e}")
        raise


def get_answer(question):
    global current_document
    if current_document is None:
        return "No document has been uploaded yet."

    try:
        # Create a vector store with only the current document
        vector_store = Chroma.from_documents(
            current_document,
            embedding,
            collection_name="current_document"
        )

        # Retrieve similar documents
        similar_docs = vector_store.similarity_search(question, k=3)

        # Combine similar document contexts
        context = " ".join([doc.page_content for doc in similar_docs])

        # Use OpenAI to generate an answer based on the context
        full_prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        answer = llm(full_prompt)

        return answer.strip()
    except Exception as e:
        print(f"Error in get_answer: {e}")
        raise