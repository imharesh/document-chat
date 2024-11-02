from fastapi import APIRouter, File, UploadFile, Depends
from typing import List
from models.schemas import DocumentResponse
from services.document import process_documents
from dependencies import get_rag_components

router = APIRouter()

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    rag_components: dict = Depends(get_rag_components)
):
    result = await process_documents(files, rag_components)
    return {
        "message": f"Successfully processed {result['processed_files']} files",
        "failed_files": result['failed_files']
    }