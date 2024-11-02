from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
from fastapi import HTTPException

def format_chat_history(chat_history: List[Dict[str, str]]) -> List:
    """Format chat history into LangChain message format."""
    return [
        HumanMessage(content=msg["content"]) if msg["role"] == "user"
        else AIMessage(content=msg["content"])
        for msg in chat_history
    ]

def process_question(question: str, chat_history: List[Dict[str, str]], rag_components: dict) -> dict:
    """Process a question using RAG components."""
    try:
        formatted_history = format_chat_history(chat_history)
        
        # Get relevant documents
        retriever_result = rag_components["history_aware_retriever"].invoke({
            "input": question,
            "chat_history": formatted_history
        })
        
        # Extract just the text content
        contexts = [str(doc) for doc in retriever_result]
        
        # Join contexts for the document chain
        context_text = "\n\n".join(contexts)
        
        # Generate response using document chain
        response = rag_components["document_chain"].invoke({
            "input": question,
            "chat_history": formatted_history,
            "context": context_text
        })
        
        return {
            "answer": response,
            "context": contexts
        }
        
    except Exception as e:
        print(f"Error in process_question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )