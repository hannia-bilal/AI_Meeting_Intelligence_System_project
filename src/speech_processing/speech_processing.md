# Speech Processing Module

## Overview

The Speech Processing Module is the speech-analysis component of the AI Meeting Intelligence System.

It accepts an audio or video meeting file and produces a structured result containing:

* detected language
* meeting duration
* detected speakers
* timestamped transcript segments
* speaker assignment for each transcript segment
* speaker-assignment confidence

The output is designed to be consumed by higher-level meeting-intelligence modules such as summarization, action-item extraction, decision detection, topic analysis, and meeting insights.

---

## Pipeline

```text
Audio / Video
     |
     v
Media Processing
     |
     v
Standard WAV Audio
     |
     +----------------+
     |                |
     v                v
Transcription     Speaker Diarization
(Whisper)         (pyannote)
     |                |
     +-------+--------+
             |
             v
      Speaker Alignment
             |
             v
    Structured JSON Result
```

---

## Components

### `media/processor.py`

Responsible for extracting and preparing standardized audio from the input media.

Input:

```text
audio/video file
```

Output:

```text
standard WAV audio
```

This component may depend on the system-level FFmpeg executable if media conversion is implemented through FFmpeg.

---

### `transcription/whisper.py`

Uses Faster-Whisper for automatic speech recognition.

It produces:

* detected language
* transcript text
* start timestamp
* end timestamp

Faster-Whisper is a Python dependency and is generally platform-independent at the package level. However, actual performance and installation behavior can vary depending on the operating system, CPU architecture, Python version, and whether CPU or GPU execution is used.

---

### `diarization/speaker.py`

Uses pyannote speaker diarization to identify speaker regions.

Example:

```text
[0.00 - 4.32] SPEAKER_01
[4.32 - 8.71] SPEAKER_02
[8.71 - 12.20] SPEAKER_01
```

The current project configuration supports a known speaker count and currently uses:

```python
num_speakers=5
```

Pyannote is a Python dependency, but its installation and runtime behavior depend on the compatible PyTorch and TorchAudio versions, operating system, CPU/GPU configuration, and Python version.

---

### `alignment/aligner.py`

Associates transcript segments with diarized speaker segments.

It calculates the temporal overlap internally and assigns:

* speaker ID
* confidence level

Internal diagnostic values such as `overlap` and `overlap_ratio` are not exposed in the final result.

This component uses standard Python logic and is platform-independent.

---

### `service.py`

This is the public entry point for the entire Speech Processing Module.

Higher-level modules should use this service instead of directly importing Whisper, pyannote, or the alignment implementation.

Example:

```python
from speech_processing.service import SpeechProcessingService

service = SpeechProcessingService(
    whisper_model="small",
    num_speakers=5,
)

result = service.process(
    "meeting.mp4"
)
```

---

## Input

The service accepts an audio or video file:

```python
result = service.process("meeting.mp3")
```

or:

```python
result = service.process("meeting.mp4")
```

The input is converted to standardized WAV audio internally when required.

Supported input formats depend on the installed media-processing tools and codecs. For reliable audio and video conversion, FFmpeg should be installed and available in the system `PATH`.

---

## Output

The service returns a JSON-serializable Python dictionary.

Example:

```json
{
  "language": "en",
  "total_duration": 60.07,
  "speakers": [
    "SPEAKER_01",
    "SPEAKER_02",
    "SPEAKER_03",
    "SPEAKER_04",
    "SPEAKER_05"
  ],
  "segments": [
    {
      "speaker_id": "SPEAKER_01",
      "start": 0.0,
      "end": 6.68,
      "text": "Welcome to the meeting.",
      "confidence": "high"
    }
  ]
}
```

### Output fields

| Field            | Type   | Description                                |
| ---------------- | ------ | ------------------------------------------ |
| `language`       | string | Detected language code                     |
| `total_duration` | number | Actual processed audio duration in seconds |
| `speakers`       | array  | Detected speaker IDs                       |
| `segments`       | array  | Timestamped speaker-attributed transcript  |
| `speaker_id`     | string | Speaker associated with segment            |
| `start`          | number | Segment start time in seconds              |
| `end`            | number | Segment end time in seconds                |
| `text`           | string | Transcript text                            |
| `confidence`     | string | Speaker assignment confidence              |

Confidence values:

```text
high
medium
low
```

If a transcript cannot be reliably associated with a speaker:

```text
speaker_id = "UNKNOWN"
```

---

## Integration With Higher-Level Modules

The higher-level AI Meeting Intelligence system should treat this module as a black-box speech service.

Recommended integration:

```python
from speech_processing.service import SpeechProcessingService


speech_service = SpeechProcessingService(
    whisper_model="small",
    num_speakers=5,
)

speech_result = speech_service.process(
    meeting_file
)
```

The returned object can then be passed to higher-level processing:

```python
meeting_result = speech_service.process(
    meeting_file
)

summary = summarization_service.generate(
    meeting_result
)

action_items = action_item_service.extract(
    meeting_result
)

decisions = decision_service.extract(
    meeting_result
)
```

The higher-level modules should not depend on:

```text
Whisper
pyannote
MediaProcessor
TranscriptAligner
```

They should depend only on the structured speech-processing result.

---

## Suggested High-Level Architecture

```text
                    Meeting Audio/Video
                            |
                            v
                +------------------------+
                | Speech Processing      |
                | Service                |
                +-----------+------------+
                            |
                            v
                  Structured Meeting
                       Transcript
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
     Summarization     Action Items       Decisions
          |                 |                  |
          +-----------------+------------------+
                            |
                            v
                   Meeting Intelligence
                            |
                            v
                         API/UI
```

---

## Configuration

Create a `.env` file:

```env
HF_TOKEN=your_huggingface_token
```

Do not commit `.env`.

Use `.env.example` as the template:

```env
HF_TOKEN=
```

`HF_TOKEN` is required to access the Hugging Face pyannote diarization model.

Before running the diarization pipeline, ensure that:

1. You have a Hugging Face account.
2. You have created an access token.
3. You have accepted the required model terms.
4. The token is available through the `HF_TOKEN` environment variable.

---

## Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt
```

The project has both Python dependencies and system-level dependencies.

### Platform-independent Python dependencies

These packages are installed through `requirements.txt` and are intended to work across supported operating systems:

| Package          | Purpose                                       | Platform notes                                                          |
| ---------------- | --------------------------------------------- | ----------------------------------------------------------------------- |
| `faster-whisper` | Speech-to-text transcription                  | Python package; runtime performance depends on CPU/GPU and architecture |
| `pyannote.audio` | Speaker diarization                           | Python package; depends on compatible PyTorch/audio libraries           |
| `python-dotenv`  | Loads environment variables from `.env`       | Platform-independent                                                    |
| `torch`          | Machine-learning runtime used by pyannote     | Package installation may vary by operating system and CPU/GPU           |
| `torchaudio`     | Audio utilities used by the PyTorch ecosystem | Must be compatible with the installed PyTorch version                   |

The Python packages are conceptually platform-independent, but machine-learning and audio packages may use different wheels or installation commands depending on:

* operating system
* CPU architecture
* Python version
* CPU versus CUDA/GPU execution
* installed driver versions
* PyTorch build

### Platform-dependent system requirements

The following dependencies are installed outside Python:

| Dependency                                | Purpose                               | Platform notes                                          |
| ----------------------------------------- | ------------------------------------- | ------------------------------------------------------- |
| FFmpeg                                    | Audio/video conversion and extraction | Must be installed separately and available in `PATH`    |
| NVIDIA CUDA toolkit or compatible runtime | Optional GPU acceleration             | Required only for supported NVIDIA GPU configurations   |
| NVIDIA GPU driver                         | Optional GPU acceleration             | Required when using CUDA-enabled execution              |
| Apple Metal/MPS support                   | Optional macOS acceleration           | Depends on supported Apple hardware and PyTorch support |

FFmpeg is not normally installed through `requirements.txt`.

Verify FFmpeg:

```bash
ffmpeg -version
```

If the command is not found, install FFmpeg using the operating system's package manager.

### Linux

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

### macOS

Using Homebrew:

```bash
brew install ffmpeg
```

### Windows

Install FFmpeg using a trusted package manager such as:

```bash
winget install Gyan.FFmpeg
```

Then reopen the terminal and verify:

```bash
ffmpeg -version
```

---

## `requirements.txt`

The recommended direct Python dependencies are:

```text
# Speech-to-text
faster-whisper==1.2.1

# Speaker diarization
pyannote.audio==4.0.7

# PyTorch ecosystem
torch
torchaudio

# Environment configuration
python-dotenv==1.2.3
```

The `faster-whisper`, `pyannote.audio`, and `python-dotenv` packages are direct application dependencies.

`torch` and `torchaudio` are included because they are required by the diarization stack, but their exact installation may need to be selected according to the target platform and execution mode.

For example:

* CPU-only installation may use CPU-compatible PyTorch packages.
* NVIDIA GPU installation may require CUDA-compatible PyTorch packages.
* macOS may use a PyTorch build compatible with Apple hardware.
* Different operating systems may require different package wheels.

Do not add every transitive dependency manually unless there is a specific reason. Packages such as `numpy`, `scipy`, `transformers`, `huggingface-hub`, `ctranslate2`, `tokenizers`, `torchcodec`, and related libraries are normally installed automatically as dependencies.

---

## Platform-Specific Installation Guidance

### CPU-only installation

The current transcription configuration uses:

```python
device="cpu"
compute_type="int8"
```

For a CPU-only environment:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This is the simplest setup and is suitable for development and environments without a GPU.

### NVIDIA GPU installation

For NVIDIA GPU execution, install a PyTorch build compatible with the installed CUDA runtime before installing or validating the remaining dependencies.

The exact command depends on:

* operating system
* Python version
* CUDA version
* GPU model

After installation, verify CUDA availability:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If the result is:

```text
True
```

the PyTorch installation can access CUDA.

The application configuration must also be changed from CPU mode to a compatible CUDA configuration.

### macOS

On macOS, CPU execution is the safest default:

```python
device="cpu"
compute_type="int8"
```

Some Apple systems may support PyTorch MPS acceleration, but this should be tested separately because model support and performance can vary.

### Windows

Windows supports the Python dependencies, but FFmpeg must be installed separately and added to `PATH`.

For CPU execution, use the standard virtual-environment installation process.

For NVIDIA GPU execution, install a compatible CUDA-enabled PyTorch build and verify it with:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Python Version

Use a supported Python version consistently across development and deployment.

Recommended versions:

```text
Python 3.10
Python 3.11
Python 3.12
```

Python 3.11 is recommended for this project because it provides a good balance between package compatibility and long-term support.

Create a virtual environment:

### Linux/macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## CPU Configuration

The current transcription configuration uses:

```python
device="cpu"
compute_type="int8"
```

The default Whisper model is:

```text
small
```

This configuration is intended to provide a practical CPU-based balance between processing speed and transcription quality.

CPU execution is generally more portable across operating systems than GPU execution, although processing speed depends on the processor and available memory.

---

## Environment Variables

Required environment variable:

```env
HF_TOKEN=your_huggingface_token
```

Example `.env.example`:

```env
HF_TOKEN=
```

Do not commit `.env` to source control.

The `.env` file is platform-independent, but environment-variable loading depends on how the application is started. The application should load it through `python-dotenv` or through the deployment environment.

---

## Testing

The development/integration pipeline can be run with:

```bash
python test_pipeline.py
```

This validates:

1. audio extraction
2. transcription
3. speaker diarization
4. speaker-transcript alignment
5. final structured result

`test_pipeline.py` is a development/testing entry point and should not be used as the API for higher-level modules.

Before testing, verify:

```bash
python --version
ffmpeg -version
```

Also verify the Python packages:

```bash
python -c "import torch; print('Torch:', torch.__version__)"
python -c "import torchaudio; print('TorchAudio:', torchaudio.__version__)"
python -c "import faster_whisper; print('Faster-Whisper: OK')"
python -c "import pyannote.audio; print('Pyannote: OK')"
```

---

## Reproducible Environments

Use `requirements.txt` for direct project dependencies.

After successfully testing the complete pipeline, create a lock file containing the exact installed versions:

```bash
pip freeze > requirements.lock.txt
```

Recommended files:

```text
requirements.txt
requirements.lock.txt
```

`requirements.txt` describes the direct dependencies required by the project.

`requirements.lock.txt` records the exact package versions tested in a specific environment.

Because PyTorch and related machine-learning packages can be platform-specific, a separate lock file may be needed for different deployment targets, for example:

```text
requirements-cpu-linux.txt
requirements-cpu-windows.txt
requirements-cuda.txt
requirements-macos.txt
```

Only create separate platform-specific files if the project is deployed on multiple platforms and the package sets differ.

---

## Public Interface

The intended public interface is:

```python
SpeechProcessingService.process(
    input_file
)
```

Input:

```text
audio/video path
```

Output:

```text
JSON-serializable dictionary
```

This interface should remain stable so that higher-level modules can be developed independently from the underlying speech-processing implementation.
