from typing import List, Dict, Any, Optional
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings
from app.utils.logger import logger

class RAGRetriever:
    def __init__(self, vector_store: Optional[VectorStore] = None, embedding_service: Optional[EmbeddingService] = None):
        self.vector_store = vector_store or VectorStore()
        self.embedding_service = embedding_service or EmbeddingService()

    def retrieve(self, query: str, top_k: int = settings.TOP_K_EVIDENCE, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant chunks for a textual query."""
        emb = self.embedding_service.get_embedding(query)
        results = self.vector_store.query(query_embedding=emb, top_k=top_k, category=category)
        logger.info(f"RAG retrieved {len(results)} chunks for query: '{query[:60]}...'")
        return results

    def retrieve_for_profile(self, profile: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """Synthesize a rich ecological query from an environmental profile and retrieve evidence."""
        query_parts = []
        if profile.get("soil_organic_carbon") is not None:
            query_parts.append(f"soil organic carbon {profile['soil_organic_carbon']}% microbial diversity")
        if profile.get("annual_rainfall_mm") is not None:
            query_parts.append(f"annual rainfall {profile['annual_rainfall_mm']}mm drought moisture stress")
        if profile.get("crop_type"):
            query_parts.append(f"{profile['crop_type']} monoculture intercropping agroforestry")
        if profile.get("land_use"):
            query_parts.append(f"{profile['land_use']} habitat biodiversity")
        if profile.get("pesticide_usage"):
            query_parts.append(f"pesticide {profile['pesticide_usage']} pollinator health decline")
        if profile.get("region"):
            query_parts.append(f"{profile['region']} semi-arid dryland restoration")

        combined_query = " ".join(query_parts) if query_parts else "soil organic carbon biodiversity land restoration"
        return self.retrieve(query=combined_query, top_k=top_k)
