from pathlib import Path

from faster_whisper import WhisperModel


class TranscriptionService:

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_file: Path):

        segments, info = self.model.transcribe(
            str(audio_file),
        )

        results = []

        for segment in segments:
            results.append(
                {
                    "start": float(segment.start),
                    "end": float(segment.end),
                    "text": segment.text.strip(),
                }
            )

        return {
            "language": info.language,
            "segments": results,
        }