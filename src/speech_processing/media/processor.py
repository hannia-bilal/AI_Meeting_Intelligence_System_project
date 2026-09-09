import subprocess
from pathlib import Path


class MediaProcessor:

    def extract_audio(
        self,
        input_file: Path,
        output_file: Path,
    ) -> Path:

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_file),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(output_file),
        ]

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )

        return output_file