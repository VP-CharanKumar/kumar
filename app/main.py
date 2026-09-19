from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.api import api_router
from app.database.init_db import init_database
from app.rag.ingest import ingest_knowledge_base
from app.utils.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Scientific intelligence for healthier ecosystems — Knowledge-Grounded Multi-Metric Environmental Reasoning Platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router)

# Mount frontend static files if directory exists
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    logger.info("Booting Darukaa.Earth AI Biodiversity Intelligence System...")
    init_database()
    # Ingest knowledge into ChromaDB / Vector Store if needed
    try:
        ingest_knowledge_base(force_reindex=False)
    except Exception as e:
        logger.warning(f"Background knowledge ingestion encountered warning: {e}")
    logger.info("Darukaa.Earth system startup sequence completed.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
