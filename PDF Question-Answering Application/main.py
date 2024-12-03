from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the PDF Question-Answering API"}

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
