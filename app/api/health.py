from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.rag.vector_store import VectorStore
from app.config import settings

router = APIRouter(prefix="/api", tags=["Health"])

@router.get("/health", response_model=HealthResponse)
def get_health():
    store = VectorStore(settings.CHROMA_PATH)
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        database="sqlite_connected",
        rag_chunks_indexed=store.count(),
        environment=settings.APP_ENV
    )
