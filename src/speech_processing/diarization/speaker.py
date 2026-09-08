import os
from pathlib import Path

from dotenv import load_dotenv
from pyannote.audio import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class DiarizationService:

    def __init__(self):
        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError(
                "HF_TOKEN environment variable is not set."
            )

        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            token=token,
        )

    def diarize(
        self,
        audio_file: Path,
        num_speakers: int | None = None,
    ):
        if num_speakers is not None:
            output = self.pipeline(
                str(audio_file),
                num_speakers=num_speakers,
            )
        else:
            output = self.pipeline(
                str(audio_file),
            )

        results = []

        for segment, speaker in output.speaker_diarization:
            results.append(
                {
                    "speaker_id": speaker,
                    "start": float(segment.start),
                    "end": float(segment.end),
                }
            )

        return results