"""
The core "Ask AI" orchestration:
  question -> embed -> retrieve top-k chunks for this meeting -> LLM answer
  -> map cited excerpts back to real timestamps -> log conversation -> return

This is the single entry point Faez's API layer (and routes.py below) calls.
"""
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.embeddings import embed_texts, embed_query
from app.chunking import build_chunks
from app.vector_search import index_chunks, search_similar_chunks
from app.llm_service import generate_answer
from app.models import QAConversation
from app.schemas import (
    TranscriptSegmentIn,
    TimestampReference,
    AskResponse,
    IndexMeetingResponse,
)


def index_meeting_transcript(
    db: Session, meeting_id: uuid.UUID, segments: List[TranscriptSegmentIn]
) -> IndexMeetingResponse:
    """
    Called once Taskeen's pipeline finishes transcribing + diarizing a
    meeting. Chunks the transcript, embeds each chunk, and stores it for
    later retrieval. Safe to re-run if a meeting is reprocessed.
    """
    chunks = build_chunks(segments)
    embeddings = embed_texts([c.text for c in chunks])
    chunk_count = index_chunks(db, meeting_id, list(zip(chunks, embeddings)))
    return IndexMeetingResponse(meeting_id=meeting_id, chunks_indexed=chunk_count)


def ask_meeting_question(
    db: Session, meeting_id: uuid.UUID, question: str, user_id: uuid.UUID | None
) -> AskResponse:
    query_vec = embed_query(question)
    top_chunks = search_similar_chunks(db, meeting_id, query_vec)

    result = generate_answer(question, top_chunks)
    used_indices = result["used_excerpt_indices"] or list(range(len(top_chunks)))

    references = [
        TimestampReference(
            start_time_seconds=top_chunks[i].start_time_seconds,
            end_time_seconds=top_chunks[i].end_time_seconds,
            speaker=top_chunks[i].speaker,
            snippet=top_chunks[i].text[:200],
        )
        for i in used_indices
        if 0 <= i < len(top_chunks)
    ]

    # Persist to AI Conversations table (per Database Requirements)
    db.add(
        QAConversation(
            meeting_id=meeting_id,
            user_id=user_id,
            question=question,
            answer=result["answer"],
            cited_timestamps=str([r.dict() for r in references]),
        )
    )
    db.commit()

    return AskResponse(
        meeting_id=meeting_id,
        question=question,
        answer=result["answer"],
        timestamp_references=references,
    )
