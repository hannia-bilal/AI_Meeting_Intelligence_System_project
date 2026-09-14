import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models import Base, MeetingChunk, QAConversation  # noqa: F401

__all__ = ["Base", "MeetingChunk", "QAConversation"]
