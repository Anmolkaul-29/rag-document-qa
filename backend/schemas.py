from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    query: str

class ResetRequest(BaseModel):
    session_id: str
