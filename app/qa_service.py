import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa_service import ask_meeting_question, index_meeting_transcript  # noqa: F401

__all__ = ["ask_meeting_question", "index_meeting_transcript"]
