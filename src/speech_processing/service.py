from pathlib import Path
import json
import wave

from media.processor import MediaProcessor
from transcription.whisper import TranscriptionService
from diarization.speaker import DiarizationService
from alignment.aligner import TranscriptAligner


class SpeechProcessingService:

    def __init__(
        self,
        whisper_model: str = "small",
        num_speakers: int = 5,
    ):
        self.num_speakers = num_speakers

        self.media_processor = MediaProcessor()

        self.transcription_service = TranscriptionService(
            model_size=whisper_model,
            device="cpu",
            compute_type="int8",
        )

        self.diarization_service = DiarizationService()

        self.aligner = TranscriptAligner()

    def _get_audio_duration(
        self,
        audio_file: Path,
    ) -> float:

        with wave.open(str(audio_file), "rb") as wav:

            frames = wav.getnframes()
            sample_rate = wav.getframerate()

            if sample_rate == 0:
                return 0.0

            return frames / float(sample_rate)

    def process(
        self,
        input_file: str | Path,
    ) -> dict:

        input_file = Path(input_file)

        if not input_file.exists():
            raise FileNotFoundError(
                f"Input file not found: {input_file}"
            )

        # ----------------------------------------------------
        # 1. Prepare standard audio
        # ----------------------------------------------------

        temp_dir = Path("temp")
        temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_audio = (
            temp_dir /
            f"{input_file.stem}.wav"
        )

        self.media_processor.extract_audio(
            input_file,
            output_audio,
        )

        # ----------------------------------------------------
        # 2. Get actual audio duration
        # ----------------------------------------------------

        duration = self._get_audio_duration(
            output_audio
        )

        # ----------------------------------------------------
        # 3. Transcription
        # ----------------------------------------------------

        transcription = (
            self.transcription_service.transcribe(
                output_audio
            )
        )

        language = transcription["language"]

        transcript_segments = (
            transcription["segments"]
        )

        # ----------------------------------------------------
        # 4. Speaker diarization
        # ----------------------------------------------------

        diarization_segments = (
            self.diarization_service.diarize(
                output_audio,
                num_speakers=self.num_speakers,
            )
        )

        # ----------------------------------------------------
        # 5. Get speaker list
        # ----------------------------------------------------

        speakers = sorted(
            {
                segment["speaker_id"]
                for segment in diarization_segments
            }
        )

        # ----------------------------------------------------
        # 6. Align transcript with speakers
        # ----------------------------------------------------

        aligned_segments = self.aligner.align(
            transcript_segments,
            diarization_segments,
        )

        # ----------------------------------------------------
        # 7. Clean final segments
        # ----------------------------------------------------

        clean_segments = []

        for segment in aligned_segments:

            clean_segments.append(
                {
                    "speaker_id": segment["speaker_id"],
                    "start": round(
                        segment["start"],
                        2,
                    ),
                    "end": round(
                        segment["end"],
                        2,
                    ),
                    "text": segment["text"],
                    "confidence": segment["confidence"],
                }
            )

        # ----------------------------------------------------
        # 8. Final structured result
        # ----------------------------------------------------

        return {
            "language": language,
            "total_duration": round(
                duration,
                2,
            ),
            "speakers": speakers,
            "segments": clean_segments,
        }

    def process_to_json(
        self,
        input_file: str | Path,
    ) -> str:

        result = self.process(input_file)

        return json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )