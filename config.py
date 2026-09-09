"""
Configuration for the Meeting Q&A + Vector Search module.

All values are read from environment variables so this module can be dropped
into the shared backend (Faez's FastAPI app) without hardcoding secrets.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Database (shared PostgreSQL instance, per project architecture) ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/meeting_intel",
    )

    # --- Embeddings ---
    # Local model by default (no API key / cost needed for embeddings).
    # Swap to an API-based embedder later by changing EMBEDDING_PROVIDER.
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "local")
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "384"))  # matches MiniLM-L6-v2

    # --- LLM for answer generation (RAG) ---
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # --- Chunking ---
    CHUNK_MAX_CHARS: int = int(os.getenv("CHUNK_MAX_CHARS", "800"))
    CHUNK_OVERLAP_CHARS: int = int(os.getenv("CHUNK_OVERLAP_CHARS", "150"))

    # --- Retrieval ---
    TOP_K: int = int(os.getenv("TOP_K", "5"))


settings = Settings()
