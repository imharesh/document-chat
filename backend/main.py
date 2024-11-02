from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from api.v1 import chat, document

def create_application() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        chat.router,
        prefix=f"{settings.API_V1_STR}/chat",
        tags=["chat"]
    )
    app.include_router(
        document.router,
        prefix=f"{settings.API_V1_STR}/documents",
        tags=["documents"]
    )
    
    return app

app = create_application()