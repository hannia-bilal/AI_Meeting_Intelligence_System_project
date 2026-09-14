import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from embeddings import embed_query, embed_texts  # noqa: F401

__all__ = ["embed_texts", "embed_query"]
