import unittest
from pathlib import Path
from app.rag.document_loader import DocumentLoader
from app.rag.chunker import MarkdownChunker
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import RAGRetriever
from app.config import settings

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.loader = DocumentLoader(settings.KNOWLEDGE_DIR)
        self.chunker = MarkdownChunker(target_chunk_size=500, overlap=80)
        self.embedder = EmbeddingService()
        self.store = VectorStore(settings.CHROMA_PATH)
        self.retriever = RAGRetriever(self.store, self.embedder)

    def test_load_documents(self):
        docs = self.loader.load_documents()
        self.assertGreaterEqual(len(docs), 10, "Should load at least 10 knowledge files")
        for d in docs:
            self.assertIn("filename", d)
            self.assertIn("content", d)
            self.assertGreater(len(d["content"]), 100)

    def test_chunking(self):
        sample_doc = {
            "filename": "soil_health.md",
            "title": "Soil Health & SOC Dynamics",
            "category": "soil_science",
            "content": "# Soil Organic Carbon\n\nSOC is fundamental.\n\n## Microbial Stabilization\n\nGlomalin aggregates soil particles."
        }
        chunks = self.chunker.chunk_document(sample_doc)
        self.assertGreaterEqual(len(chunks), 1)
        for c in chunks:
            self.assertIn("chunk_id", c)
            self.assertIn("content", c)

    def test_embeddings_and_retrieval(self):
        emb = self.embedder.get_embedding("Soil organic carbon in semi-arid wheat monoculture")
        self.assertIn(len(emb), [256, 768])
        
        results = self.retriever.retrieve("soil organic carbon and water holding capacity", top_k=3)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("title", results[0])
        self.assertIn("content", results[0])

if __name__ == "__main__":
    unittest.main()
