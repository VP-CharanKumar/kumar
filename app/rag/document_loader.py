import json
from pathlib import Path
from typing import List, Dict, Any
from app.config import settings
from app.utils.logger import logger

class DocumentLoader:
    def __init__(self, knowledge_dir: Path = settings.KNOWLEDGE_DIR):
        self.knowledge_dir = knowledge_dir

    def load_documents(self) -> List[Dict[str, Any]]:
        """Load all markdown documents and metadata from the knowledge base."""
        documents = []
        if not self.knowledge_dir.exists():
            logger.warning(f"Knowledge directory {self.knowledge_dir} does not exist.")
            return documents

        # Load sources.json for canonical attribution
        sources_map = {}
        sources_file = self.knowledge_dir / "sources.json"
        if sources_file.exists():
            try:
                with open(sources_file, "r", encoding="utf-8") as f:
                    sources_data = json.load(f)
                    for item in sources_data:
                        sources_map[item.get("id")] = item
            except Exception as e:
                logger.error(f"Failed to parse sources.json: {e}")

        # Iterate all markdown files
        for md_file in sorted(self.knowledge_dir.glob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
                # Derive category and title
                category = md_file.stem
                lines = content.splitlines()
                title = lines[0].replace("#", "").strip() if lines and lines[0].startswith("#") else category.replace("_", " ").title()
                
                documents.append({
                    "filename": md_file.name,
                    "filepath": str(md_file),
                    "category": category,
                    "title": title,
                    "content": content,
                    "source_type": "scientific_markdown"
                })
            except Exception as e:
                logger.error(f"Error loading {md_file}: {e}")

        logger.info(f"Loaded {len(documents)} knowledge documents from {self.knowledge_dir}.")
        return documents
