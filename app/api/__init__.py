from fastapi import APIRouter
from .health import router as health_router
from .chat import router as chat_router
from .analyze import router as analyze_router
from .conversations import router as conversations_router
from .knowledge import router as knowledge_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(analyze_router)
api_router.include_router(conversations_router)
api_router.include_router(knowledge_router)

__all__ = ["api_router"]
