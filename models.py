"""
ORM models owned by the Q&A + Vector Search module.

NOTE on integration: `meeting_id` below is a foreign key into Hassan's
`meetings` table. We don't redefine that table here — we just reference its
primary key by convention (UUID or int, matching his schema). Confirm the
exact column type with Hassan before running migrations together.
"""
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.config import settings


class MeetingChunk(Base):
    """
    A chunk of a meeting transcript, embedded for semantic search.

    Populated after Taskeen's speech-to-text + speaker ID pipeline finishes
    and the transcript is saved to the shared DB. This table is what makes
    "Ask AI" possible — it's the retrieval index for a single meeting.
    """
    __tablename__ = "meeting_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    chunk_index = Column(Integer, nullable=False)  # order within the meeting
    speaker = Column(String(120), nullable=True)   # from Taskeen's diarization
    text = Column(Text, nullable=False)

    start_time_seconds = Column(Float, nullable=False)  # for "jump to timestamp"
    end_time_seconds = Column(Float, nullable=False)

    embedding = Column(Vector(settings.EMBEDDING_DIM), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class QAConversation(Base):
    """
    Logs each question/answer pair for a meeting's "Ask AI" chat, so the
    conversation persists across page reloads (per Database Requirements:
    'AI Conversations').
    """
    __tablename__ = "qa_conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)  # who asked

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    # Stored as a JSON-ish string of [{start, end, speaker, snippet}, ...]
    # kept simple (Text) here; swap to JSONB if the shared DB already uses it.
    cited_timestamps = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
