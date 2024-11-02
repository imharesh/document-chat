from fastapi import APIRouter, Depends
from models.schemas import QuestionRequest, QuestionResponse
from services.chat import process_question
from dependencies import get_rag_components

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    query: QuestionRequest,
    rag_components: dict = Depends(get_rag_components)
):
    return process_question(
        question=query.question,
        chat_history=query.chat_history,
        rag_components=rag_components
    )
