"""
Integration tests for Meeting Intelligence Analyzer & Service.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
import pytest
from pathlib import Path

from src.ai_intelligence.schemas import MeetingAnalysisRequest, MeetingIntelligenceReport
from src.ai_intelligence.providers.mock_provider import MockLLMProvider
from src.ai_intelligence.analyzer import MeetingIntelligenceAnalyzer
from src.ai_intelligence.service import MeetingIntelligenceService

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_analyzer_on_taskeen_sample():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    provider = MockLLMProvider()
    analyzer = MeetingIntelligenceAnalyzer(provider=provider)
    req = MeetingAnalysisRequest(**data)

    report: MeetingIntelligenceReport = analyzer.analyze(req)

    # 1. Title
    assert report.title is not None
    assert len(report.title) > 0

    # 2. Summaries
    assert report.summary.executive_summary is not None
    assert len(report.summary.executive_summary) > 20
    assert report.summary.detailed_summary is not None

    # 3. Participants & Speaker metrics
    assert len(report.participants) == 2
    spk0 = next(p for p in report.participants if p.speaker_id == "SPEAKER_00")
    spk1 = next(p for p in report.participants if p.speaker_id == "SPEAKER_01")
    assert spk0.spoken_seconds > 0
    assert spk1.spoken_seconds > 0
    assert (spk0.contribution_percentage + spk1.contribution_percentage) > 0

    # 4. Key discussion points
    assert len(report.key_points) > 0
    assert report.key_points[0].topic is not None
    assert report.key_points[0].timestamp is not None

    # 5. Decisions
    assert len(report.decisions) > 0
    assert report.decisions[0].decision is not None
    assert report.decisions[0].timestamp is not None

    # 6. Action items & deadline normalization
    assert len(report.action_items) > 0
    action = report.action_items[0]
    assert action.task is not None
    assert action.assigned_to is not None
    assert action.deadline_raw is not None
    assert action.deadline_normalized is not None  # Successfully resolved to ISO YYYY-MM-DD
    assert action.timestamp is not None

    # 7. Deadlines list
    assert len(report.deadlines) > 0
    assert report.deadlines[0].item is not None

    # 8. Unresolved issues & Follow-ups
    assert len(report.unresolved_issues) > 0
    assert len(report.follow_ups) > 0

    # 9. Sentiment analysis
    assert report.sentiment.overall_sentiment is not None
    assert -1.0 <= report.sentiment.score <= 1.0
    assert len(report.sentiment.tone_summary) > 0

    # 10. Speaker-wise Transcript
    assert len(report.speaker_wise_transcript) == 4
    seg0 = report.speaker_wise_transcript[0]
    assert seg0.speaker_id == "SPEAKER_00"
    assert seg0.timestamp_formatted == "02:15"
    assert "launch the website" in seg0.text

    # 11. Dashboard Metrics
    assert report.dashboard_metrics is not None
    assert report.dashboard_metrics.duration_formatted == "30m 45s"
    assert report.dashboard_metrics.action_items_count == len(report.action_items)
    assert report.dashboard_metrics.decisions_count == len(report.decisions)

    # 12. Metadata
    assert report.metadata.total_duration_seconds == 1845.0
    assert report.metadata.total_segments == 4
    assert report.metadata.model_name == "mock-intelligence-v1"
    assert report.metadata.processing_time_seconds >= 0


def test_speaker_name_overrides():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["speaker_name_overrides"] = {
        "SPEAKER_00": "Custom Leader Name",
        "SPEAKER_01": "Custom Engineer Name"
    }

    service = MeetingIntelligenceService(provider=MockLLMProvider())
    report = service.analyze_meeting_sync(data)

    p0 = next(p for p in report.participants if p.speaker_id == "SPEAKER_00")
    assert p0.detected_name == "Custom Leader Name"
    assert report.speaker_wise_transcript[0].speaker_name == "Custom Leader Name"


@pytest.mark.asyncio
async def test_service_async_execution_and_database_mapping():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    service = MeetingIntelligenceService(provider=MockLLMProvider())
    report = await service.analyze_meeting(data)

    assert isinstance(report, MeetingIntelligenceReport)

    # Test DB helper for Hassan Raza
    db_records = service.to_database_records(report, meeting_id="meet_12345")
    assert db_records["meeting_id"] == "meet_12345"
    assert "meeting_updates" in db_records
    assert "action_items" in db_records
    assert "decisions" in db_records
    assert "participants" in db_records
    assert "speaker_wise_transcript" in db_records
    assert "dashboard_metrics" in db_records
    assert len(db_records["action_items"]) > 0


@pytest.mark.asyncio
async def test_service_ask_question():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    service = MeetingIntelligenceService(provider=MockLLMProvider())
    qa_ans = await service.ask_question(
        segments=data.get("segments", []),
        question="What did we decide about the launch date?"
    )

    assert qa_ans.question == "What did we decide about the launch date?"
    assert len(qa_ans.answer) > 0
    assert len(qa_ans.relevant_timestamps) > 0
    assert qa_ans.relevant_timestamps[0].formatted == "02:29"
