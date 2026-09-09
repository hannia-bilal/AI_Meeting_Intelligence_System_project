"""
Unit tests for transcript chunking and speaker metrics.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

from src.ai_intelligence.schemas import TranscriptSegment
from src.ai_intelligence.chunker import (
    calculate_speaker_metrics,
    format_transcript_for_prompt,
    chunk_transcript
)


def test_speaker_metrics_calculation():
    segments = [
        TranscriptSegment(speaker="SPEAKER_00", start=0.0, end=30.0, text="First statement"),
        TranscriptSegment(speaker="SPEAKER_01", start=30.0, end=90.0, text="Second statement"),
        TranscriptSegment(speaker="SPEAKER_00", start=90.0, end=120.0, text="Third statement"),
    ]

    metrics = calculate_speaker_metrics(segments, total_duration=120.0)

    # 2 distinct speakers
    assert len(metrics) == 2

    spk0 = next(p for p in metrics if p.speaker_id == "SPEAKER_00")
    spk1 = next(p for p in metrics if p.speaker_id == "SPEAKER_01")

    # SPEAKER_00: 30 + 30 = 60s (50%)
    assert spk0.spoken_seconds == 60.0
    assert spk0.contribution_percentage == 50.0
    assert spk0.turn_count == 2

    # SPEAKER_01: 60s (50%)
    assert spk1.spoken_seconds == 60.0
    assert spk1.contribution_percentage == 50.0
    assert spk1.turn_count == 1


def test_format_transcript_for_prompt():
    segments = [
        TranscriptSegment(speaker="SPEAKER_00", start=135.2, end=141.8, text="We should launch next week.")
    ]
    formatted = format_transcript_for_prompt(segments)
    assert "[02:15] SPEAKER_00: We should launch next week." in formatted


def test_chunk_transcript_splitting():
    # Create 10 segments of 50 words each = 500 words
    sample_text = "word " * 50
    segments = [
        TranscriptSegment(speaker=f"SPEAKER_{i%2}", start=float(i*10), end=float((i+1)*10), text=sample_text)
        for i in range(10)
    ]

    # Max 120 words per chunk should yield multiple chunks
    chunks = chunk_transcript(segments, max_words_per_chunk=120, overlap_segments=1)
    assert len(chunks) > 1
    # Check that all original segments are covered
    total_unique_starts = set(s.start for c in chunks for s in c)
    assert len(total_unique_starts) == 10
