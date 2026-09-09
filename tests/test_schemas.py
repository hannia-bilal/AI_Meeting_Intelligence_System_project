"""
Unit tests for AI Intelligence schemas and data models.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
import pytest
from pathlib import Path
from pydantic import ValidationError

from src.ai_intelligence.schemas import (
    MeetingAnalysisRequest,
    TranscriptSegment,
    MeetingIntelligenceReport,
    SummaryType,
    SentimentCategory,
    TaskPriority
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_taskeen_whatsapp_schema_loads_successfully():
    """
    Validates that the exact format proposed by Taskeen in WhatsApp and approved by Hannia
    validates perfectly against MeetingAnalysisRequest.
    """
    fixture_path = FIXTURES_DIR / "sample_taskeen_transcript.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    req = MeetingAnalysisRequest(**data)
    assert req.duration == 1845.0
    assert req.language == "en"
    assert len(req.segments) == 4
    assert req.segments[0].speaker == "SPEAKER_00"
    assert req.segments[0].start == 135.2
    assert req.segments[0].end == 141.8
    assert "launch the website" in req.segments[0].text


def test_invalid_segment_fails_validation():
    """
    Ensures missing required fields like speaker or start time trigger validation errors.
    """
    with pytest.raises(ValidationError):
        TranscriptSegment(text="Missing speaker and timestamps")


def test_empty_segments_fails_validation():
    """
    Ensures an empty segments list is rejected.
    """
    with pytest.raises(ValidationError):
        MeetingAnalysisRequest(
            duration=100.0,
            language="en",
            segments=[]
        )
