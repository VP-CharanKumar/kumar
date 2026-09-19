#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.ingest import ingest_knowledge_base
from app.utils.logger import logger

def main():
    logger.info("=== Starting Knowledge Ingestion Pipeline ===")
    result = ingest_knowledge_base(force_reindex=True)
    logger.info(f"Ingestion Result: {result}")
    print("\n------------------------------------------------------------")
    print("KNOWLEDGE INGESTION SUMMARY:")
    print(f"Status: {result.get('status')}")
    print(f"Documents processed: {result.get('documents_processed', 0)}")
    print(f"Chunks indexed: {result.get('chunks_indexed', 0)}")
    print(f"Total vector database size: {result.get('total_store_count', 0)}")
    print("------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
