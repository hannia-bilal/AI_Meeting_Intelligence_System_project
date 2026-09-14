"""Compatibility package for the shared FastAPI backend integration.

This project is organized as top-level modules, but the rest of the team and
standard FastAPI conventions expect imports like `from app.config import settings`.
The root-level modules are imported here as a compatibility layer so the backend
can be mounted cleanly into the unified app.
"""

__all__ = [
    "config",
    "database",
    "models",
    "schemas",
    "routes",
    "qa_service",
    "chunking",
    "embeddings",
    "vector_search",
    "llm_service",
    "main",
]
