"""
Data schemas for the AI Meeting Intelligence module.
Author: Muhammad Awais (AI Meeting Intelligence)
Project: AI Meeting Intelligence System

Defines Pydantic models for:
- Input Contract: Matches Speech Processing (Taskeen Mustafa) transcript output
- Output Contract: Structured Meeting Intelligence Report (Summaries, Actions, Decisions, etc.)
- Helper and sub-models for serialization, DB mapping, and API responses
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ==============================================================================
# Enums
# ==============================================================================

class SummaryType(str, Enum):
    SHORT = "short"
    DETAILED = "detailed"
    BOTH = "both"


class SentimentCategory(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ==============================================================================
# Input Schemas (Speech Processing -> AI Intelligence)
# ==============================================================================

class TranscriptSegment(BaseModel):
    """
    Individual spoken segment from Speech Processing (Taskeen Mustafa).
    Matches WhatsApp agreed schema:
    speaker: "SPEAKER_00"
    start: 135.2 (seconds)
    end: 141.8 (seconds)
    text: "We should launch the website next week."
    """
    speaker: str = Field(
        ...,
        description="Speaker identifier label (e.g., 'SPEAKER_00', 'SPEAKER_01')",
        examples=["SPEAKER_00"]
    )
    start: float = Field(
        ...,
        description="Start timestamp in seconds",
        ge=0.0,
        examples=[135.2]
    )
    end: float = Field(
        ...,
        description="End timestamp in seconds",
        ge=0.0,
        examples=[141.8]
    )
    text: str = Field(
        ...,
        description="Transcribed text for this segment",
        examples=["We should launch the website next week."]
    )

    model_config = ConfigDict(extra="ignore")


class MeetingAnalysisRequest(BaseModel):
    """
    Complete transcript payload received from Speech Processing / Backend.
    """
    duration: float = Field(
        ...,
        description="Total duration of the meeting in seconds",
        ge=0.0,
        examples=[1845.0]
    )
    language: str = Field(
        default="en",
        description="Detected or specified spoken language code (e.g., 'en')",
        examples=["en"]
    )
    segments: List[TranscriptSegment] = Field(
        ...,
        description="Chronological list of transcript segments",
        min_length=1
    )
    meeting_title: Optional[str] = Field(
        default=None,
        description="Optional pre-existing meeting title or topic"
    )
    meeting_date: Optional[str] = Field(
        default=None,
        description="Reference date of the meeting in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS) used to resolve relative deadlines like 'tomorrow' or 'Friday'"
    )
    summary_type: SummaryType = Field(
        default=SummaryType.BOTH,
        description="Requested summary depth: 'short', 'detailed', or 'both'"
    )

    model_config = ConfigDict(extra="ignore")


# ==============================================================================
# Output Schemas (AI Intelligence -> Backend / DB / Q&A / Frontend)
# ==============================================================================

class TimestampReference(BaseModel):
    """
    Reference to a point or span in the meeting recording.
    """
    seconds: float = Field(..., description="Timestamp in seconds", ge=0.0)
    formatted: str = Field(..., description="Formatted timestamp (HH:MM:SS or MM:SS)", examples=["02:15", "01:14:32"])


class ParticipantDetail(BaseModel):
    """
    Information about an identified speaker/participant.
    """
    speaker_id: str = Field(..., description="Speaker label from transcript (e.g., 'SPEAKER_00')")
    detected_name: Optional[str] = Field(
        default=None,
        description="Real name if naturally mentioned during conversation (e.g. 'Ali', 'Hassan')"
    )
    spoken_seconds: float = Field(default=0.0, description="Total speaking time in seconds")
    contribution_percentage: float = Field(default=0.0, description="Percentage of total talk time", ge=0.0, le=100.0)
    turn_count: int = Field(default=0, description="Number of times speaker took the floor")


class KeyDiscussionPoint(BaseModel):
    """
    A key point or topic discussed during the meeting.
    """
    topic: str = Field(..., description="Short topic title")
    summary: str = Field(..., description="Explanation of what was discussed")
    timestamp: Optional[TimestampReference] = Field(default=None, description="Timestamp where this point arose")
    speaker: Optional[str] = Field(default=None, description="Primary speaker or initiator")


class DecisionItem(BaseModel):
    """
    A decision finalized or agreed upon during the meeting.
    """
    decision: str = Field(..., description="The decision made")
    rationale: Optional[str] = Field(default=None, description="Context or reason for this decision")
    timestamp: Optional[TimestampReference] = Field(default=None, description="Timestamp where decision was made")
    agreed_by: List[str] = Field(default_factory=list, description="Speakers or participants who agreed")


class ActionItem(BaseModel):
    """
    An assigned action item or task extracted from the conversation.
    """
    task: str = Field(..., description="Description of the task to be done")
    assigned_to: str = Field(..., description="Person, role, or team assigned (e.g., 'Ali', 'SPEAKER_01', 'Frontend Team')")
    assigned_speaker_id: Optional[str] = Field(default=None, description="Speaker ID if mapped (e.g., 'SPEAKER_01')")
    deadline_raw: Optional[str] = Field(default=None, description="Raw deadline mention (e.g., 'Friday', 'next Monday', 'September 10')")
    deadline_normalized: Optional[str] = Field(default=None, description="Standardized ISO date (YYYY-MM-DD) calculated from meeting reference date")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Inferred task priority")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Initial status of the action item")
    timestamp: Optional[TimestampReference] = Field(default=None, description="Timestamp where task was assigned or stated")


class DeadlineItem(BaseModel):
    """
    Timeline milestone or deadline detected naturally in the discussion.
    """
    item: str = Field(..., description="Deliverable or milestone name")
    raw_text: str = Field(..., description="Natural language phrasing (e.g., 'end of this month')")
    normalized_date: Optional[str] = Field(default=None, description="Standardized ISO date (YYYY-MM-DD)")
    context: Optional[str] = Field(default=None, description="Relevant meeting context")


class UnresolvedIssue(BaseModel):
    """
    Open question, blocker, or item left undecided.
    """
    issue: str = Field(..., description="Description of the unresolved matter")
    context: Optional[str] = Field(default=None, description="Context or differing opinions raised")
    urgency: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Urgency of resolution")
    timestamp: Optional[TimestampReference] = Field(default=None, description="Timestamp where issue was discussed")


class FollowUpItem(BaseModel):
    """
    Item or topic that requires subsequent check-in or next meeting follow-up.
    """
    item: str = Field(..., description="What needs to be followed up on")
    suggested_owner: Optional[str] = Field(default=None, description="Recommended person or role to lead follow-up")
    suggested_timeframe: Optional[str] = Field(default=None, description="When to follow up (e.g., 'next sprint', 'in 2 days')")


class SentimentAnalysis(BaseModel):
    """
    Meeting sentiment and conversational tone breakdown.
    """
    overall_sentiment: SentimentCategory = Field(
        default=SentimentCategory.NEUTRAL,
        description="Overall sentiment category (positive, neutral, negative, mixed)"
    )
    score: float = Field(
        default=0.0,
        description="Sentiment score ranging from -1.0 (very negative) to +1.0 (very positive)",
        ge=-1.0,
        le=1.0
    )
    positive_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    neutral_percentage: float = Field(default=100.0, ge=0.0, le=100.0)
    negative_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    tone_summary: str = Field(
        default="",
        description="Qualitative summary of the team dynamics, tone, and collaboration level"
    )


class MeetingSummary(BaseModel):
    """
    Meeting summary containing both short executive summary and detailed summary.
    """
    executive_summary: str = Field(
        ...,
        description="High-level 1-2 paragraph executive summary covering the meeting essence"
    )
    detailed_summary: str = Field(
        ...,
        description="Comprehensive summary structured by key topics and chronological themes"
    )
    summary_type_provided: SummaryType = Field(
        default=SummaryType.BOTH,
        description="Summary depth provided"
    )


class MeetingMetadata(BaseModel):
    """
    Processing metadata and stats.
    """
    total_duration_seconds: float
    total_segments: int
    word_count: int
    language: str
    model_name: str
    processing_time_seconds: float
    chunk_count: int = 1
    analyzed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class MeetingIntelligenceReport(BaseModel):
    """
    Complete Master Intelligence Report generated by Muhammad Awais's module.
    Delivers every requirement specified in the project documentation:
    - Meeting title
    - Executive & Detailed summaries
    - Participants & speaker metrics
    - Speaker-wise transcript
    - Key discussion points
    - Decisions made
    - Action items & task owners
    - Deadlines (raw & normalized)
    - Unresolved issues
    - Follow-up items
    - Overall meeting sentiment
    """
    title: str = Field(..., description="Descriptive meeting title generated by AI")
    summary: MeetingSummary
    participants: List[ParticipantDetail] = Field(default_factory=list)
    key_points: List[KeyDiscussionPoint] = Field(default_factory=list)
    decisions: List[DecisionItem] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    deadlines: List[DeadlineItem] = Field(default_factory=list)
    unresolved_issues: List[UnresolvedIssue] = Field(default_factory=list)
    follow_ups: List[FollowUpItem] = Field(default_factory=list)
    sentiment: SentimentAnalysis
    metadata: MeetingMetadata

    model_config = ConfigDict(extra="ignore")
