from pathlib import Path
from typing import Dict, Any
from app.rag.document_loader import DocumentLoader
from app.rag.chunker import MarkdownChunker
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings
from app.utils.logger import logger

def ingest_knowledge_base(force_reindex: bool = False) -> Dict[str, Any]:
    """Ingest knowledge files into ChromaDB / Vector Store."""
    loader = DocumentLoader(settings.KNOWLEDGE_DIR)
    chunker = MarkdownChunker()
    embedder = EmbeddingService()
    store = VectorStore(settings.CHROMA_PATH)

    current_count = store.count()
    if current_count > 0 and not force_reindex:
        logger.info(f"Vector store already populated with {current_count} chunks. Skipping re-ingestion.")
        return {
            "status": "already_indexed",
            "chunks_indexed": current_count,
            "message": f"Knowledge base already contains {current_count} indexed chunks."
        }

    docs = loader.load_documents()
    if not docs:
        logger.warning("No knowledge documents found to ingest.")
        return {
            "status": "no_documents",
            "chunks_indexed": 0,
            "message": "No markdown files found in knowledge directory."
        }

    all_chunks = []
    for doc in docs:
        chunks = chunker.chunk_document(doc)
        all_chunks.extend(chunks)

    logger.info(f"Extracted {len(all_chunks)} semantic chunks from {len(docs)} documents. Generating embeddings...")

    # Generate embeddings
    embeddings = []
    for idx, c in enumerate(all_chunks):
        emb = embedder.get_embedding(c["content"])
        embeddings.append(emb)
        if (idx + 1) % 10 == 0 or idx == len(all_chunks) - 1:
            logger.info(f"Embedded {idx + 1}/{len(all_chunks)} chunks...")

    store.add_documents(all_chunks, embeddings)
    total = store.count()
    logger.info(f"Ingestion complete. Total vector store chunks: {total}")

    return {
        "status": "success",
        "documents_processed": len(docs),
        "chunks_indexed": len(all_chunks),
        "total_store_count": total,
        "message": f"Successfully indexed {len(all_chunks)} chunks across {len(docs)} knowledge domains."
    }

if __name__ == "__main__":
    ingest_knowledge_base(force_reindex=True)
