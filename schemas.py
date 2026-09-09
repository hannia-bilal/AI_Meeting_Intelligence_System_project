"""Pydantic schemas — the request/response contract for Faez's backend."""
import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class TranscriptSegmentIn(BaseModel):
    """
    One segment of Taskeen's speaker-labeled transcript output.
    This is the expected input shape for indexing a meeting.
    """
    speaker: Optional[str] = None
    text: str
    start_time_seconds: float
    end_time_seconds: float


class IndexMeetingRequest(BaseModel):
    meeting_id: uuid.UUID
    segments: List[TranscriptSegmentIn] = Field(
        ..., description="Full speaker-wise transcript for this meeting"
    )


class IndexMeetingResponse(BaseModel):
    meeting_id: uuid.UUID
    chunks_indexed: int


class AskRequest(BaseModel):
    meeting_id: uuid.UUID
    question: str
    user_id: Optional[uuid.UUID] = None


class TimestampReference(BaseModel):
    start_time_seconds: float
    end_time_seconds: float
    speaker: Optional[str] = None
    snippet: str


class AskResponse(BaseModel):
    meeting_id: uuid.UUID
    question: str
    answer: str
    timestamp_references: List[TimestampReference]
