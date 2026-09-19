import json
from pathlib import Path
from app.database.connection import engine, Base, SessionLocal
from app.models.database import KnowledgeSourceModel
from app.utils.logger import logger
from app.config import settings

def init_database():
    """Create all SQLite tables and seed canonical scientific knowledge sources."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified / initialized successfully.")
    
    # Seed sources from knowledge/sources.json if empty
    db = SessionLocal()
    try:
        count = db.query(KnowledgeSourceModel).count()
        if count == 0:
            sources_file = settings.KNOWLEDGE_DIR / "sources.json"
            if sources_file.exists():
                with open(sources_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    source = KnowledgeSourceModel(
                        source_id=item.get("id"),
                        title=item.get("title"),
                        organization=item.get("organization"),
                        year=item.get("year", 2020),
                        category=item.get("category", "general"),
                        summary=item.get("summary", ""),
                        doi_or_url=item.get("doi_or_url", ""),
                        evidence_level=item.get("evidence_level", "High")
                    )
                    db.add(source)
                db.commit()
                logger.info(f"Seeded {len(data)} scientific knowledge sources into SQLite database.")
    except Exception as e:
        logger.error(f"Error seeding knowledge sources into database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
