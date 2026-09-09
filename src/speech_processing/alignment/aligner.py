class TranscriptAligner:

    def __init__(
        self,
        min_overlap_ratio: float = 0.50,
        boundary_tolerance: float = 0.50,
    ):
        self.min_overlap_ratio = min_overlap_ratio
        self.boundary_tolerance = boundary_tolerance

    def align(self, transcript_segments, diarization_segments):
        results = []

        for transcript in transcript_segments:

            transcript_start = float(transcript["start"])
            transcript_end = float(transcript["end"])

            transcript_duration = (
                transcript_end - transcript_start
            )

            best_speaker = None
            best_overlap = 0.0

            # Ignore invalid transcript segments
            if transcript_duration <= 0:
                results.append(
                    {
                        "speaker_id": "UNKNOWN",
                        "start": transcript_start,
                        "end": transcript_end,
                        "text": transcript["text"],
                        "overlap": 0.0,
                        "overlap_ratio": 0.0,
                        "confidence": "low",
                    }
                )
                continue

            for speaker in diarization_segments:

                speaker_start = (
                    speaker["start"] - self.boundary_tolerance
                )

                speaker_end = (
                    speaker["end"] + self.boundary_tolerance
                )

                overlap_start = max(
                    transcript_start,
                    speaker_start,
                )

                overlap_end = min(
                    transcript_end,
                    speaker_end,
                )

                overlap = max(
                    0.0,
                    overlap_end - overlap_start,
                )

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = speaker["speaker_id"]

            overlap_ratio = (
                best_overlap / transcript_duration
            )

            if overlap_ratio < self.min_overlap_ratio:
                best_speaker = "UNKNOWN"

            if overlap_ratio >= 0.75:
                confidence = "high"
            elif overlap_ratio >= 0.50:
                confidence = "medium"
            else:
                confidence = "low"

            results.append(
                {
                    "speaker_id": best_speaker or "UNKNOWN",
                    "start": transcript_start,
                    "end": transcript_end,
                    "text": transcript["text"],
                    "overlap": round(best_overlap, 3),
                    "overlap_ratio": round(overlap_ratio, 3),
                    "confidence": confidence,
                }
            )

        return results