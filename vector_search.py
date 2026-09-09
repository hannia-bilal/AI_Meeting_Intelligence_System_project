"""
Vector similarity search against the meeting_chunks table using pgvector.

Retrieval is scoped to a single meeting_id — the "Ask AI" feature is
explicitly per-meeting per the spec ("A contextual AI chat based only on
the selected meeting"), not a cross-meeting search.
"""
from typing import List
import uuid

from sqlalchemy.orm import Session

from app.models import MeetingChunk
from app.config import settings


def index_chunks(db: Session, meeting_id: uuid.UUID, chunks_with_embeddings) -> int:
    """
    Persists chunks + their embeddings for a meeting.
    `chunks_with_embeddings` is a list of (TranscriptChunk, embedding_vector) tuples.
    Replaces any existing chunks for the meeting (re-indexing is idempotent).
    """
    db.query(MeetingChunk).filter(MeetingChunk.meeting_id == meeting_id).delete()

    count = 0
    for chunk, embedding in chunks_with_embeddings:
        db.add(
            MeetingChunk(
                meeting_id=meeting_id,
                chunk_index=chunk.chunk_index,
                speaker=chunk.speaker,
                text=chunk.text,
                start_time_seconds=chunk.start_time_seconds,
                end_time_seconds=chunk.end_time_seconds,
                embedding=embedding,
            )
        )
        count += 1

    db.commit()
    return count


def search_similar_chunks(
    db: Session, meeting_id: uuid.UUID, query_embedding: List[float], top_k: int = None
) -> List[MeetingChunk]:
    """
    Returns the top-k most semantically similar chunks for this meeting,
    ranked by cosine distance (pgvector's `<=>` operator via the ORM helper).
    """
    top_k = top_k or settings.TOP_K
    return (
        db.query(MeetingChunk)
        .filter(MeetingChunk.meeting_id == meeting_id)
        .order_by(MeetingChunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )
