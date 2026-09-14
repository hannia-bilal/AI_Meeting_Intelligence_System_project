import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas import (  # noqa: F401
    AskRequest,
    AskResponse,
    IndexMeetingRequest,
    IndexMeetingResponse,
    TimestampReference,
    TranscriptSegmentIn,
)

__all__ = [
    "TranscriptSegmentIn",
    "IndexMeetingRequest",
    "IndexMeetingResponse",
    "AskRequest",
    "AskResponse",
    "TimestampReference",
]
