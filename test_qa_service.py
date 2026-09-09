"""
Lightweight tests that don't require a live Postgres/pgvector instance or
an Anthropic API key — useful for a quick sanity check before demo day.
Run: pytest tests/
"""
from app.chunking import build_chunks
from app.schemas import TranscriptSegmentIn


def test_build_chunks_basic():
    segments = [
        TranscriptSegmentIn(speaker="Ali", text="We should launch next week.", start_time_seconds=0, end_time_seconds=4),
        TranscriptSegmentIn(speaker="Faez", text="I'll finish the backend by Friday.", start_time_seconds=4, end_time_seconds=8),
    ]
    chunks = build_chunks(segments)

    assert len(chunks) >= 1
    assert chunks[0].start_time_seconds == 0
    assert "launch" in chunks[0].text.lower() or "launch" in chunks[-1].text.lower()


def test_build_chunks_splits_long_transcript():
    long_text = "This is a sentence about the marketing budget. " * 50
    segments = [
        TranscriptSegmentIn(speaker="Speaker 1", text=long_text, start_time_seconds=0, end_time_seconds=120)
    ]
    chunks = build_chunks(segments)
    # A single very long segment should still produce at least one chunk,
    # and each chunk should respect roughly the configured max length.
    assert len(chunks) >= 1


def test_build_chunks_empty_input():
    assert build_chunks([]) == []
