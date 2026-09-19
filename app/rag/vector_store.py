import os
import json
import math
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.config import settings
from app.utils.logger import logger

class VectorStore:
    def __init__(self, persist_dir: str = settings.CHROMA_PATH):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = "darukaa_biodiversity_knowledge"
        self.chroma_client = None
        self.chroma_collection = None
        self.fallback_file = self.persist_dir / "knowledge_index.json"
        self._fallback_records: List[Dict[str, Any]] = []
        
        self._init_chroma()
        self._load_fallback()

    def _init_chroma(self):
        try:
            import chromadb
            self.chroma_client = chromadb.PersistentClient(path=str(self.persist_dir))
            self.chroma_collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Initialized ChromaDB persistent client at {self.persist_dir}.")
        except Exception as e:
            logger.warning(f"ChromaDB native backend unavailable ({e}). Using persistent JSON vector store.")

    def _load_fallback(self):
        if self.fallback_file.exists():
            try:
                with open(self.fallback_file, "r", encoding="utf-8") as f:
                    self._fallback_records = json.load(f)
            except Exception as e:
                logger.error(f"Error reading fallback vector file: {e}")
                self._fallback_records = []

    def _save_fallback(self):
        try:
            with open(self.fallback_file, "w", encoding="utf-8") as f:
                json.dump(self._fallback_records, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving fallback vector file: {e}")

    def add_documents(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Store chunk records and embeddings."""
        if not chunks:
            return

        # 1. Store in ChromaDB if present
        if self.chroma_collection:
            try:
                ids = [c["chunk_id"] for c in chunks]
                documents = [c["content"] for c in chunks]
                metadatas = [{
                    "filename": c.get("filename", ""),
                    "category": c.get("category", ""),
                    "title": c.get("title", ""),
                    "section": c.get("section", ""),
                    "word_count": c.get("word_count", 0)
                } for c in chunks]
                
                # Upsert to avoid duplicate index errors
                self.chroma_collection.upsert(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
            except Exception as e:
                logger.error(f"ChromaDB upsert error ({e}), synchronizing to persistent fallback store.")

        # 2. Always maintain the persistent fallback store
        existing_ids = {r["chunk_id"] for r in self._fallback_records}
        for chunk, emb in zip(chunks, embeddings):
            record = {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "title": chunk.get("title", ""),
                "category": chunk.get("category", ""),
                "filename": chunk.get("filename", ""),
                "section": chunk.get("section", ""),
                "embedding": emb
            }
            if chunk["chunk_id"] in existing_ids:
                # Update
                self._fallback_records = [r if r["chunk_id"] != chunk["chunk_id"] else record for r in self._fallback_records]
            else:
                self._fallback_records.append(record)
                existing_ids.add(chunk["chunk_id"])

        self._save_fallback()
        logger.info(f"Indexed {len(chunks)} chunks in vector store (total: {len(self._fallback_records)}).")

    def count(self) -> int:
        if self.chroma_collection:
            try:
                return self.chroma_collection.count()
            except Exception:
                pass
        return len(self._fallback_records)

    def query(self, query_embedding: List[float], top_k: int = 5, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query nearest neighbors by cosine similarity."""
        # Try ChromaDB first
        if self.chroma_collection:
            try:
                where_filter = {"category": category} if category else None
                res = self.chroma_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=where_filter
                )
                if res and res.get("ids") and res["ids"][0]:
                    results = []
                    for i in range(len(res["ids"][0])):
                        cid = res["ids"][0][i]
                        doc = res["documents"][0][i]
                        meta = res["metadatas"][0][i] if res.get("metadatas") else {}
                        dist = res["distances"][0][i] if res.get("distances") else 0.5
                        # Chroma cosine distance is 1 - similarity
                        score = max(0.0, 1.0 - dist)
                        results.append({
                            "chunk_id": cid,
                            "content": doc,
                            "title": meta.get("title", ""),
                            "category": meta.get("category", ""),
                            "filename": meta.get("filename", ""),
                            "section": meta.get("section", ""),
                            "score": round(score, 4),
                            "metadata": meta
                        })
                    return results
            except Exception as e:
                logger.debug(f"Chroma query failed ({e}), using local cosine search.")

        # Local cosine similarity search
        scored = []
        for r in self._fallback_records:
            if category and r.get("category") != category:
                continue
            emb = r.get("embedding", [])
            if not emb or len(emb) != len(query_embedding):
                continue
            
            # Dot product (embeddings are normalized)
            dot = sum(a * b for a, b in zip(query_embedding, emb))
            scored.append({
                "chunk_id": r["chunk_id"],
                "content": r["content"],
                "title": r.get("title", ""),
                "category": r.get("category", ""),
                "filename": r.get("filename", ""),
                "section": r.get("section", ""),
                "score": round(max(0.0, min(1.0, dot)), 4),
                "metadata": {
                    "filename": r.get("filename"),
                    "category": r.get("category"),
                    "title": r.get("title"),
                    "section": r.get("section")
                }
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
