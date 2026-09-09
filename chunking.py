"""
Turns Taskeen's speaker-wise transcript segments into retrieval-friendly
chunks, preserving timestamps and speaker labels so we can always point
the user back to the exact moment in the recording.

Strategy: greedily pack consecutive segments (same general context) up to
CHUNK_MAX_CHARS, so each chunk stays coherent for embedding/retrieval,
without cutting a sentence across two unrelated chunks. A small character
overlap is kept between consecutive chunks so context isn't lost at chunk
boundaries.
"""
from dataclasses import dataclass
from typing import List

from app.config import settings
from app.schemas import TranscriptSegmentIn


@dataclass
class TranscriptChunk:
    chunk_index: int
    speaker: str | None
    text: str
    start_time_seconds: float
    end_time_seconds: float


def build_chunks(segments: List[TranscriptSegmentIn]) -> List[TranscriptChunk]:
    if not segments:
        return []

    chunks: List[TranscriptChunk] = []
    buffer_text = ""
    buffer_start = segments[0].start_time_seconds
    buffer_end = segments[0].start_time_seconds
    buffer_speaker = segments[0].speaker
    chunk_index = 0

    def flush():
        nonlocal buffer_text, chunk_index
        if buffer_text.strip():
            chunks.append(
                TranscriptChunk(
                    chunk_index=chunk_index,
                    speaker=buffer_speaker,
                    text=buffer_text.strip(),
                    start_time_seconds=buffer_start,
                    end_time_seconds=buffer_end,
                )
            )
            chunk_index += 1

    for seg in segments:
        line = f"{seg.speaker + ': ' if seg.speaker else ''}{seg.text}"

        # If a single speaker turn changes, or the buffer is getting long,
        # start a new chunk (keeping a small text overlap for continuity).
        would_exceed = len(buffer_text) + len(line) + 1 > settings.CHUNK_MAX_CHARS

        if would_exceed and buffer_text:
            flush()
            overlap = buffer_text[-settings.CHUNK_OVERLAP_CHARS:]
            buffer_text = overlap + " " + line
            buffer_start = seg.start_time_seconds
            buffer_speaker = seg.speaker
        else:
            if not buffer_text:
                buffer_start = seg.start_time_seconds
                buffer_speaker = seg.speaker
            buffer_text = (buffer_text + " " + line).strip()

        buffer_end = seg.end_time_seconds

    flush()
    return chunks
