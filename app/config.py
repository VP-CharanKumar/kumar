import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "Darukaa.Earth AI Biodiversity Intelligence"
    VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    
    # Gemini API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/darukaa.db")
    
    # ChromaDB Vector Store
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))
    
    # Knowledge directory
    KNOWLEDGE_DIR: Path = BASE_DIR / "knowledge"
    
    # Models
    GEMINI_REASONING_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"
    
    # Reasoning Parameters
    MIN_VARIABLES_FOR_REASONING: int = 3
    TOP_K_EVIDENCE: int = 5

settings = Settings()
