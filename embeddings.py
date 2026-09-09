"""
Embedding generation, abstracted behind a single function so the rest of
the module doesn't care which provider is used.

Default: sentence-transformers/all-MiniLM-L6-v2, run locally.
  - No API key needed, no per-call cost — good for a 1-week project deadline.
  - 384-dim vectors (matches settings.EMBEDDING_DIM).

To switch to an API-based embedding model later (e.g. OpenAI text-embedding-3),
implement `_embed_api` and flip EMBEDDING_PROVIDER in .env — nothing else
in the codebase needs to change.
"""
from functools import lru_cache
from typing import List

from app.config import settings


@lru_cache(maxsize=1)
def _get_local_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(settings.EMBEDDING_MODEL_NAME)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Returns one embedding vector per input text, in the same order."""
    if settings.EMBEDDING_PROVIDER == "local":
        model = _get_local_model()
        vectors = model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()

    raise NotImplementedError(
        f"Embedding provider '{settings.EMBEDDING_PROVIDER}' is not implemented. "
        "Add an _embed_api() branch here if you switch providers."
    )


def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
