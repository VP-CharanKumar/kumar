from fastapi import APIRouter, Query
from typing import Optional, Dict, Any, List
from app.rag.retriever import RAGRetriever
from app.rag.ingest import ingest_knowledge_base
from app.models.schemas import KnowledgeSearchResult

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge & RAG"])

@router.get("/search", response_model=List[KnowledgeSearchResult])
def search_knowledge(
    query: str = Query(..., description="Semantic search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    top_k: int = Query(5, ge=1, le=20)
):
    retriever = RAGRetriever()
    raw_results = retriever.retrieve(query=query, top_k=top_k, category=category)
    return [
        KnowledgeSearchResult(
            chunk_id=r["chunk_id"],
            title=r.get("title", "Scientific Resource"),
            category=r.get("category", "general"),
            source=r.get("filename", "corpus"),
            content=r["content"],
            score=r.get("score", 0.0),
            metadata=r.get("metadata", {})
        )
        for r in raw_results
    ]

@router.post("/ingest")
def trigger_ingest(force_reindex: bool = Query(False, description="Force re-indexing")):
    result = ingest_knowledge_base(force_reindex=force_reindex)
    return result
