import tempfile
import os
from typing import List, BinaryIO
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader

def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return os.path.splitext(filename.lower())[1]

def is_pdf_file(filename: str) -> bool:
    """Check if the file is a PDF."""
    return get_file_extension(filename) == '.pdf'

def validate_file_size(file: BinaryIO, max_size_mb: int = 10) -> None:
    """Validate file size."""
    file.seek(0, 2)
    file_size = file.tell() / (1024 * 1024)
    file.seek(0)
    
    if file_size > max_size_mb:
        raise HTTPException(
            status_code=413,
            detail=f"File size ({file_size:.1f}MB) exceeds maximum allowed size of {max_size_mb}MB"
        )

async def process_documents(files: List[UploadFile], rag_components: dict) -> dict:
    """Process PDF documents."""
    processed_files = 0
    failed_files = []
    vector_store = rag_components["vector_store"]
    text_splitter = rag_components["text_splitter"]
    
    for file in files:
        temp_file_path = None
        try:
            if not is_pdf_file(file.filename):
                failed_files.append({
                    "filename": file.filename,
                    "reason": "Only PDF files are supported"
                })
                continue
            
            temp_file_path = f"temp_{file.filename}"
            
            with open(temp_file_path, "wb") as temp_file:
                content = await file.read()
                validate_file_size(file.file)
                temp_file.write(content)
            
            # Load and process document
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            
            if documents:
                # Split documents into chunks
                splits = text_splitter.split_documents(documents)
                
                # Add to vector store
                texts = [doc.page_content for doc in splits]
                vector_store.add_texts(texts=texts)
                
                processed_files += 1
            
        except Exception as e:
            failed_files.append({
                "filename": file.filename,
                "reason": f"Processing error: {str(e)}"
            })
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
    
    return {
        "processed_files": processed_files,
        "failed_files": failed_files
    }