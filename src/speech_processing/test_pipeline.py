from pathlib import Path

from media.processor import MediaProcessor
from transcription.whisper import TranscriptionService
from diarization.speaker import DiarizationService
from alignment.aligner import TranscriptAligner


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path("uploads/meeting3.mp3")
OUTPUT_AUDIO = Path("temp/meeting3.wav")


# ============================================================
# STEP 1: AUDIO EXTRACTION
# ============================================================

print("\n" + "=" * 60)
print("STEP 1: AUDIO EXTRACTION")
print("=" * 60)

processor = MediaProcessor()

media_result = processor.extract_audio(
    INPUT_FILE,
    OUTPUT_AUDIO,
)

print("Audio extraction completed.")
print(f"Standard audio: {OUTPUT_AUDIO}")


# ============================================================
# STEP 2: TRANSCRIPTION
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: TRANSCRIPTION")
print("=" * 60)

transcription_service = TranscriptionService()

transcription_result = transcription_service.transcribe(
    OUTPUT_AUDIO
)

language = transcription_result["language"]
duration = transcription_result["duration"]
transcript_segments = transcription_result["segments"]

print(f"Language: {language}")
print(f"Duration: {duration:.2f} seconds")
print(f"Transcript segments: {len(transcript_segments)}")


print("\nRAW TRANSCRIPTION SEGMENTS")

for segment in transcript_segments:
    print(
        f"[{segment['start']:.3f} - {segment['end']:.3f}] "
        f"{segment['text']}"
    )


# ============================================================
# STEP 3: SPEAKER DIARIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: SPEAKER DIARIZATION")
print("=" * 60)

diarization_service = DiarizationService()

diarization_segments = diarization_service.diarize(
    OUTPUT_AUDIO,
    num_speakers=5,
)

print(
    f"Diarization segments: "
    f"{len(diarization_segments)}"
)


speakers = sorted(
    {
        segment["speaker_id"]
        for segment in diarization_segments
    }
)

print(f"Speakers detected: {len(speakers)}")

for speaker in speakers:
    print(f"  - {speaker}")


print("\nRAW DIARIZATION SEGMENTS")

for segment in diarization_segments:
    print(
        f"[{segment['start']:.3f} - {segment['end']:.3f}] "
        f"{segment['speaker_id']}"
    )


# ============================================================
# STEP 4: SPEAKER-TRANSCRIPT ALIGNMENT
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: SPEAKER-TRANSCRIPT ALIGNMENT")
print("=" * 60)

aligner = TranscriptAligner()

aligned_segments = aligner.align(
    transcript_segments,
    diarization_segments,
)


# ============================================================
# STEP 5: CLEAN FINAL RESULT
# ============================================================

clean_segments = []

for segment in aligned_segments:

    clean_segments.append(
        {
            "speaker_id": segment["speaker_id"],
            "start": round(segment["start"], 2),
            "end": round(segment["end"], 2),
            "text": segment["text"],
            "confidence": segment["confidence"],
        }
    )


final_result = {
    "language": language,
    "total_duration": round(duration, 2),
    "speakers": speakers,
    "segments": clean_segments,
}


# ============================================================
# FINAL MEETING RESULT
# ============================================================

print("\n" + "=" * 60)
print("FINAL MEETING RESULT")
print("=" * 60)

print(f"Language: {final_result['language']}")
print(
    f"Total Duration: "
    f"{final_result['total_duration']:.2f} seconds"
)
print(f"Speakers: {len(final_result['speakers'])}")

print("\nSPEAKER-WISE TRANSCRIPT")

for segment in final_result["segments"]:

    speaker_id = segment["speaker_id"]
    start = segment["start"]
    end = segment["end"]
    confidence = segment["confidence"]
    text = segment["text"]

    print(
        f"[{start:.2f} - {end:.2f}] "
        f"{speaker_id} "
        f"({confidence}): "
        f"{text}"
    )


# ============================================================
# PIPELINE COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("PIPELINE COMPLETED")
print("=" * 60)

print("\nFinal structured result:")

print(final_result)