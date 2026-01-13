# LLM-Based Document Q&A System with Conversation Memory (RAG)

## 1. Overview

This project implements a **document-based Question Answering (QA) system** using **Retrieval-Augmented Generation (RAG)**.  
The system allows users to upload documents, ask questions grounded in those documents, maintain multi-turn conversations, and interact via REST APIs suitable for frontend integration.

The solution is designed to:
- Avoid hallucinations
- Provide traceability to source documents
- Support multi-turn conversational memory
- Be easily integrated with a web UI

---

## 2. System Architecture

High-level flow:

Documents → Text Extraction → Chunking → Embeddings → Vector Database (FAISS)
↓
User Query → Retrieve Top-K Chunks → Prompt (Context + Memory) → LLM → Answer


### Key Components
- **FastAPI** – Backend API layer
- **FAISS** – Vector database for similarity search
- **SentenceTransformers** – Text embeddings
- **Together AI (Mixtral)** – Large Language Model
- **Session-based Memory** – Multi-turn conversation handling

---

## 3. Features

- 📄 Document ingestion (PDF)
- ✂️ Semantic text chunking
- 🔍 Similarity-based retrieval (Top-K)
- 🧠 LLM-based grounded answer generation
- 💬 Multi-turn conversation memory per session
- 🚫 Hallucination prevention
- 🌐 API-first design with Swagger UI

## Frontend UI

A Streamlit-based web UI is provided for:
- Uploading documents
- Asking questions
- Viewing conversation history
- Resetting sessions

The UI communicates with the backend exclusively via REST APIs, keeping the system frontend-agnostic.

---

## 4. Document Ingestion

### Supported Formats
- PDF (via `pypdf`)

### Metadata Stored
Each chunk stores:
- `doc` – Document name
- `page` – Page number

### API
POST /documents/ingest


Uploads and indexes documents into the vector database.

---

## 5. Text Chunking Strategy

- **Chunk size:** 600 characters  
- **Chunk overlap:** 100 characters  

### Justification
- Maintains semantic completeness
- Prevents loss of context at boundaries
- Optimized for LLM context windows

Chunking is implemented using a recursive text splitter to avoid breaking sentences unnaturally.

---

## 6. Embeddings & Retrieval

### Embedding Model
- `all-MiniLM-L6-v2` (SentenceTransformers)

**Why this model?**
- Lightweight and fast
- High-quality semantic embeddings
- Well-suited for document retrieval

### Vector Database
- **FAISS (IndexFlatL2)**

**Why FAISS?**
- Fast similarity search
- Local and lightweight
- Production-proven for RAG systems

### Retrieval Parameters
- **Top-K:** 8  
- **Similarity Metric:** L2 distance  

A higher Top-K value is used to improve recall, especially for multi-page documents where relevant information may appear in different sections.


---

## 7. Answer Generation with Conversation Memory

### LLM
- **Mixtral-8x7B-Instruct** via **Together AI**
- OpenAI-compatible API

### Prompt Design
The prompt enforces:
- Use of **retrieved context only**
- No external knowledge
- Explicit refusal if answer is missing

If the answer cannot be derived, the system responds with:

"Not found in the documents."


### Conversation Memory
- Stored per `session_id`
- Only the **last 3–5 turns** are included in each prompt
- Prevents prompt overflow and context dilution

### Resetting Memory

---
POST /session/reset

## 8. API Endpoints

### 1. Ingest Documents
**POST /documents/ingest**

Input: Multipart file upload  

Output:
```json
{ "status": "document ingested" }


2. Chat

POST /chat

Input:

{
  "session_id": "demo1",
  "query": "What skills does the candidate have?"
}

Output:

{
  "answer": "...",
  "sources": ["document_name.pdf"]
}

3. Reset Session
POST /session/reset


Input:

{
  "session_id": "demo1"
}

4. Root Health Check
GET /


Returns a simple status message to confirm the API is running.
---

## 9. Running the Project

1. Create Virtual Environment
python -m venv rag_env
rag_env\Scripts\activate   # Windows

2. Install Dependencies
pip install -r requirements.txt

3. Set Environment Variable

Create a .env file:

TOGETHER_API_KEY=your_api_key_here

4. Run Backend
uvicorn backend.main:app --reload

5. Open Swagger UI
http://127.0.0.1:8000/docs
---
## 10. Hallucination Prevention

The system explicitly:

Restricts LLM answers to retrieved context

Rejects unanswered questions with a fixed response

Avoids inference or assumption beyond document content

This ensures reliable, grounded answers.
---
## 11. Future Improvements

Support for DOCX and Markdown

Persistent memory store (Redis)

Hybrid search (BM25 + vectors)

Source highlighting at sentence level

Authentication and multi-user support
---
## 12. Conclusion

This project demonstrates a production-style RAG pipeline with:

Clean architecture

Strong grounding guarantees

Multi-turn conversational memory

API-first design ready for UI integration

It satisfies all requirements of an LLM-based Document Q&A system.
