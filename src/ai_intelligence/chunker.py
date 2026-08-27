"""
Transcript processor and chunker for handling long meeting recordings.
Author: Muhammad Awais (AI Meeting Intelligence)

Provides:
- Speaker statistics calculation (contribution percentage, total talk time, turn counts)
- Formatted transcript generation with timestamps and speaker tags
- Smart chunking for long meeting transcripts preserving sentence and turn integrity
"""

from typing import List, Dict, Any, Tuple
from .schemas import TranscriptSegment, ParticipantDetail
from .normalizers import format_seconds_to_timestamp


def calculate_speaker_metrics(segments: List[TranscriptSegment], total_duration: float) -> List[ParticipantDetail]:
    """
    Computes speaking metrics per speaker:
    - spoken_seconds
    - contribution_percentage
    - turn_count
    - speaker_id
    """
    stats: Dict[str, Dict[str, Any]] = {}

    for seg in segments:
        spk = seg.speaker or "SPEAKER_UNKNOWN"
        duration = max(0.0, seg.end - seg.start)
        if spk not in stats:
            stats[spk] = {
                "spoken_seconds": 0.0,
                "turn_count": 0
            }
        stats[spk]["spoken_seconds"] += duration
        stats[spk]["turn_count"] += 1

    total_spoken = sum(s["spoken_seconds"] for s in stats.values())
    effective_duration = total_duration if total_duration > 0 else (total_spoken if total_spoken > 0 else 1.0)

    participants: List[ParticipantDetail] = []
    for spk, data in sorted(stats.items()):
        spoken = round(data["spoken_seconds"], 2)
        pct = round((data["spoken_seconds"] / effective_duration) * 100.0, 2)
        participants.append(
            ParticipantDetail(
                speaker_id=spk,
                detected_name=None,  # LLM can enrich this if real name is revealed in conversation
                spoken_seconds=spoken,
                contribution_percentage=min(100.0, pct),
                turn_count=data["turn_count"]
            )
        )

    return participants


def format_transcript_for_prompt(segments: List[TranscriptSegment]) -> str:
    """
    Converts transcript segments into structured text with timestamps for LLM analysis.
    Example:
    [02:15] SPEAKER_00: We should launch the website next week.
    [02:22] SPEAKER_01: Agreed, but we need backend tests finished by Friday.
    """
    lines = []
    for seg in segments:
        ts = format_seconds_to_timestamp(seg.start)
        lines.append(f"[{ts}] {seg.speaker}: {seg.text.strip()}")
    return "\n".join(lines)


def chunk_transcript(
    segments: List[TranscriptSegment],
    max_words_per_chunk: int = 2500,
    overlap_segments: int = 2
) -> List[List[TranscriptSegment]]:
    """
    Splits long transcript segments into manageable chunks for LLMs.
    Guarantees segment boundaries are never broken in the middle of a speech turn.
    """
    if not segments:
        return []

    chunks: List[List[TranscriptSegment]] = []
    current_chunk: List[TranscriptSegment] = []
    current_word_count = 0

    for seg in segments:
        words = len(seg.text.split())
        if current_word_count + words > max_words_per_chunk and current_chunk:
            chunks.append(current_chunk)
            # Add small overlap for conversational continuity
            overlap = current_chunk[-overlap_segments:] if len(current_chunk) >= overlap_segments else current_chunk
            current_chunk = list(overlap)
            current_word_count = sum(len(s.text.split()) for s in current_chunk)

        current_chunk.append(seg)
        current_word_count += words

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
