"""
AI Meeting Intelligence Package
Author: Muhammad Awais (AI Meeting Intelligence)
Project: AI Meeting Intelligence System
"""

from .schemas import (
    TranscriptSegment,
    MeetingAnalysisRequest,
    MeetingIntelligenceReport,
    MeetingSummary,
    ParticipantDetail,
    KeyDiscussionPoint,
    DecisionItem,
    ActionItem,
    DeadlineItem,
    UnresolvedIssue,
    FollowUpItem,
    SentimentAnalysis,
    SentimentCategory,
    SummaryType,
    TaskPriority,
    TaskStatus,
    TimestampReference
)
from .normalizers import normalize_deadline, format_seconds_to_timestamp
from .chunker import calculate_speaker_metrics, format_transcript_for_prompt, chunk_transcript
from .analyzer import MeetingIntelligenceAnalyzer
from .service import MeetingIntelligenceService
from .providers import get_llm_provider, BaseLLMProvider, MockLLMProvider

__all__ = [
    "TranscriptSegment",
    "MeetingAnalysisRequest",
    "MeetingIntelligenceReport",
    "MeetingSummary",
    "ParticipantDetail",
    "KeyDiscussionPoint",
    "DecisionItem",
    "ActionItem",
    "DeadlineItem",
    "UnresolvedIssue",
    "FollowUpItem",
    "SentimentAnalysis",
    "SentimentCategory",
    "SummaryType",
    "TaskPriority",
    "TaskStatus",
    "TimestampReference",
    "normalize_deadline",
    "format_seconds_to_timestamp",
    "calculate_speaker_metrics",
    "format_transcript_for_prompt",
    "chunk_transcript",
    "MeetingIntelligenceAnalyzer",
    "MeetingIntelligenceService",
    "get_llm_provider",
    "BaseLLMProvider",
    "MockLLMProvider"
]
