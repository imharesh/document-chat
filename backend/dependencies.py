from functools import lru_cache
from services.rag import initialize_rag_components

@lru_cache
def get_rag_components():
    return initialize_rag_components()
