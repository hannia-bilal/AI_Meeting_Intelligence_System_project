import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vector_search import index_chunks, search_similar_chunks  # noqa: F401

__all__ = ["index_chunks", "search_similar_chunks"]
