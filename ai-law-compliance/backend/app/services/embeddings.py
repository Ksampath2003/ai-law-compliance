"""
Text embedding service using sentence-transformers (runs locally, no API key needed).
Swap out encode() if you want to use OpenAI or Cohere embeddings instead.
"""
from functools import lru_cache
from typing import List


@lru_cache(maxsize=1)
def _get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> List[float]:
    model = _get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_law(title: str, summary: str, full_text: str = "") -> List[float]:
    """Create a combined embedding for a law document."""
    combined = f"{title}. {summary}"
    if full_text:
        # Truncate to keep within model limits
        combined += " " + full_text[:1000]
    return embed_text(combined)
