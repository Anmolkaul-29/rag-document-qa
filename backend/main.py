from fastapi import FastAPI, UploadFile, File
from backend.ingest import ingest_document
from backend.chat import chat_with_docs
from backend.memory import reset_memory
from backend.schemas import ChatRequest, ResetRequest
import shutil
import os

app = FastAPI()

@app.post("/documents/ingest")
async def ingest(file: UploadFile = File(...)):  # 👈 FIX
    os.makedirs("data/documents", exist_ok=True)

    path = f"data/documents/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        ingest_document(path)
        return {"status": "document ingested"}
    except ValueError as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat(payload: ChatRequest):  # 👈 FIX
    answer, sources = chat_with_docs(
        payload.session_id,
        payload.query
    )
    return {"answer": answer, "sources": sources}

@app.post("/session/reset")
async def reset(payload: ResetRequest):  # 👈 FIX
    reset_memory(payload.session_id)
    return {"status": "session cleared"}

@app.get("/")
def root():
    return {"message": "RAG Document Q&A API is running"}
