from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Chatbot API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str
    CHROMA_DB_PATH: str = "./chroma_db"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()