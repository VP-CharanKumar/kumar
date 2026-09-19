import math
import re
import hashlib
from typing import List
from app.config import settings
from app.utils.logger import logger

class EmbeddingService:
    def __init__(self, dimension: int = 256):
        self.dimension = dimension
        self.gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_google_gemini_api_key_here":
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Initialized Gemini Client for embeddings.")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini Client for embeddings ({e}). Using deterministic offline embeddings.")

    def get_embedding(self, text: str) -> List[float]:
        """Compute normalized vector embedding for a string."""
        if self.gemini_client:
            try:
                # Attempt using gemini text embedding
                response = self.gemini_client.models.embed_content(
                    model=settings.GEMINI_EMBEDDING_MODEL,
                    contents=text
                )
                if hasattr(response, "embedding") and response.embedding:
                    return response.embedding.values
                elif hasattr(response, "embeddings") and response.embeddings:
                    return response.embeddings[0].values
            except Exception as e:
                logger.debug(f"Gemini embed API call failed or throttled ({e}). Falling back to local semantic vectorizer.")

        return self._compute_local_vector(text)

    def _compute_local_vector(self, text: str) -> List[float]:
        """Deterministic semantic vector representation based on feature hashing and ecological keywords."""
        vec = [0.0] * self.dimension
        words = re.findall(r'\b[a-zA-Z0-9_\-\.%]+\b', text.lower())
        
        # High-value ecological domain anchors
        eco_anchors = {
            "soil": 0, "carbon": 1, "soc": 2, "microbial": 3, "ph": 4, "organic": 5, "moisture": 6,
            "rainfall": 10, "drought": 11, "semi-arid": 12, "precipitation": 13, "temperature": 14,
            "monoculture": 20, "wheat": 21, "cereal": 22, "crop": 23, "intercropping": 24, "agroforestry": 25,
            "pollinator": 30, "pesticide": 31, "bee": 32, "floral": 33, "insecticide": 34, "refugia": 35,
            "fragmentation": 40, "connectivity": 41, "corridor": 42, "patch": 43, "forest": 44, "species": 45,
            "erosion": 50, "water": 51, "swale": 52, "catchment": 53, "fao": 60, "ipcc": 61, "ipbes": 62
        }

        for word in words:
            # Hash to index
            h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            vec[idx] += 1.0

            # Weight ecological anchors heavily for semantic precision
            if word in eco_anchors:
                anchor_idx = eco_anchors[word]
                vec[anchor_idx] += 4.0

        # L2 Normalization
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec
