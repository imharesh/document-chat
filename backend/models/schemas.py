from pydantic import BaseModel
from typing import List, Dict, Optional

class Message(BaseModel):
    role: str
    content: str

class QuestionRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]] = []

class QuestionResponse(BaseModel):
    answer: str
    sources: List[Dict] = []  # Default empty list
    context: List[str] = []   # Default empty list

class DocumentResponse(BaseModel):
    message: str
    failed_files: Optional[List[Dict[str, str]]] = []