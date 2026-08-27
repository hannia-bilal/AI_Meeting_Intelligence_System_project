"""
Core AI Meeting Intelligence Analyzer.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import time
from typing import Optional, List, Dict, Any
from .schemas import (
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
    MeetingMetadata,
    TimestampReference,
    SummaryType,
    TaskPriority,
    TaskStatus
)
from .normalizers import normalize_deadline, format_seconds_to_timestamp
from .chunker import calculate_speaker_metrics, format_transcript_for_prompt, chunk_transcript
from .prompts import SYSTEM_PROMPT, ANALYSIS_JSON_SCHEMA, build_analysis_user_prompt
from .providers.base import BaseLLMProvider


def _parse_timestamp(ts_val: Any) -> Optional[TimestampReference]:
    """
    Safely converts a timestamp representation (seconds float or MM:SS string)
    into a TimestampReference.
    """
    if ts_val is None:
        return None

    if isinstance(ts_val, dict) and "seconds" in ts_val and "formatted" in ts_val:
        return TimestampReference(seconds=float(ts_val["seconds"]), formatted=str(ts_val["formatted"]))

    if isinstance(ts_val, (int, float)):
        sec = float(ts_val)
        return TimestampReference(seconds=sec, formatted=format_seconds_to_timestamp(sec))

    if isinstance(ts_val, str):
        cleaned = ts_val.strip()
        # Parse MM:SS or HH:MM:SS
        parts = cleaned.split(":")
        try:
            if len(parts) == 2:
                sec = float(parts[0]) * 60 + float(parts[1])
                return TimestampReference(seconds=sec, formatted=cleaned)
            elif len(parts) == 3:
                sec = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                return TimestampReference(seconds=sec, formatted=cleaned)
        except ValueError:
            pass

    return None


def _find_key(d: Any, *candidates) -> Any:
    """
    Finds a key in dictionary checking multiple case variations
    (e.g., 'executive_summary', 'ExecutiveSummary', 'executiveSummary').
    """
    if not isinstance(d, dict):
        return None
    for k in candidates:
        if k in d:
            return d[k]
    lower_map = {k.lower().replace("_", ""): v for k, v in d.items()}
    for k in candidates:
        clean = k.lower().replace("_", "")
        if clean in lower_map:
            return lower_map[clean]
    return None


def _stringify_summary(val: Any, default: str = "") -> str:
    """
    Converts summary values (which may be strings or list of theme objects)
    into formatted markdown text.
    """
    if not val:
        return default
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        items = []
        for item in val:
            if isinstance(item, dict):
                theme = _find_key(item, "theme", "topic", "title") or "Discussion Point"
                details = _find_key(item, "details", "summary", "text", "description") or str(item)
                items.append(f"### {theme}\n{details}")
            else:
                items.append(str(item))
        return "\n\n".join(items)
    return str(val)


class MeetingIntelligenceAnalyzer:
    """
    Orchestrates LLM analysis, prompt injection, date normalization,
    and structured intelligence reporting.
    """

    def __init__(self, provider: BaseLLMProvider):
        self.provider = provider

    def analyze(self, request: MeetingAnalysisRequest) -> MeetingIntelligenceReport:
        """
        Executes end-to-end intelligence extraction from transcript segments.
        """
        start_time = time.time()

        # 1. Base statistics & participant calculation
        base_participants = calculate_speaker_metrics(request.segments, request.duration)
        word_count = sum(len(s.text.split()) for s in request.segments)

        # 2. Format transcript for prompt
        formatted_transcript = format_transcript_for_prompt(request.segments)

        # 3. Check for chunking if transcript is massive
        chunks = chunk_transcript(request.segments, max_words_per_chunk=3500)
        chunk_count = len(chunks)

        user_prompt = build_analysis_user_prompt(
            formatted_transcript=formatted_transcript,
            meeting_title=request.meeting_title,
            summary_type=request.summary_type,
            meeting_date=request.meeting_date
        )

        # 4. Invoke LLM provider
        raw_result = self.provider.generate_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            json_schema=ANALYSIS_JSON_SCHEMA
        )

        # 5. Enrich participants with detected names
        name_map = {}
        speaker_mappings = _find_key(raw_result, "speaker_name_mappings", "SpeakerNameMapping") or []
        for mapping in speaker_mappings:
            if isinstance(mapping, dict):
                spk_id = _find_key(mapping, "speaker_id", "speaker")
                name = _find_key(mapping, "detected_name", "name")
                if spk_id and name:
                    name_map[spk_id] = name

        for p in base_participants:
            if p.speaker_id in name_map:
                p.detected_name = name_map[p.speaker_id]

        # 6. Parse and normalize Action Items & Deadlines
        action_items: List[ActionItem] = []
        raw_actions = _find_key(raw_result, "action_items", "ActionItemsTaskOwners", "action_items_task_owners") or []
        for item in raw_actions:
            if not isinstance(item, dict):
                continue
            raw_deadline = _find_key(item, "deadline_raw", "deadline", "deadline_raw_text")
            norm_deadline = normalize_deadline(raw_deadline, request.meeting_date)
            ts = _parse_timestamp(_find_key(item, "timestamp", "time"))

            # Determine priority enum
            priority_str = str(_find_key(item, "priority") or "medium").lower()
            priority = TaskPriority.MEDIUM
            if "high" in priority_str:
                priority = TaskPriority.HIGH
            elif "low" in priority_str:
                priority = TaskPriority.LOW

            action_items.append(
                ActionItem(
                    task=_find_key(item, "task", "action", "description") or "Untitled Task",
                    assigned_to=_find_key(item, "assigned_to", "owner", "assignee") or "Unassigned",
                    assigned_speaker_id=_find_key(item, "assigned_speaker_id", "speaker_id"),
                    deadline_raw=raw_deadline,
                    deadline_normalized=norm_deadline,
                    priority=priority,
                    status=TaskStatus.PENDING,
                    timestamp=ts
                )
            )

        # 7. Parse Deadlines
        deadlines: List[DeadlineItem] = []
        raw_deadlines = _find_key(raw_result, "deadlines", "DeadlinesMilestones", "deadlines_milestones") or []
        for d in raw_deadlines:
            if not isinstance(d, dict):
                continue
            raw_text = _find_key(d, "raw_text", "deadline", "date") or ""
            norm_date = normalize_deadline(raw_text, request.meeting_date)
            deadlines.append(
                DeadlineItem(
                    item=_find_key(d, "item", "task", "milestone") or "Milestone",
                    raw_text=raw_text,
                    normalized_date=norm_date,
                    context=_find_key(d, "context", "notes")
                )
            )

        # 8. Parse Key Points
        key_points: List[KeyDiscussionPoint] = []
        raw_points = _find_key(raw_result, "key_points", "KeyDiscussionPoints", "key_discussion_points") or []
        for kp in raw_points:
            if not isinstance(kp, dict):
                continue
            key_points.append(
                KeyDiscussionPoint(
                    topic=_find_key(kp, "topic", "title", "point") or "Discussion Point",
                    summary=_find_key(kp, "summary", "description", "details") or "",
                    timestamp=_parse_timestamp(_find_key(kp, "timestamp", "time")),
                    speaker=_find_key(kp, "speaker", "speaker_id")
                )
            )

        # 9. Parse Decisions
        decisions: List[DecisionItem] = []
        raw_decisions = _find_key(raw_result, "decisions", "DecisionsMade", "decisions_made") or []
        for dec in raw_decisions:
            if not isinstance(dec, dict):
                continue
            decisions.append(
                DecisionItem(
                    decision=_find_key(dec, "decision", "agreement", "title") or "",
                    rationale=_find_key(dec, "rationale", "reason", "context"),
                    timestamp=_parse_timestamp(_find_key(dec, "timestamp", "time")),
                    agreed_by=_find_key(dec, "agreed_by", "participants") or []
                )
            )

        # 10. Parse Unresolved Issues
        unresolved: List[UnresolvedIssue] = []
        raw_unresolved = _find_key(raw_result, "unresolved_issues", "UnresolvedIssuesBlockers", "unresolved_issues_blockers") or []
        for u in raw_unresolved:
            if not isinstance(u, dict):
                continue
            urgency_str = str(_find_key(u, "urgency", "priority") or "medium").lower()
            urgency = TaskPriority.HIGH if "high" in urgency_str else (TaskPriority.LOW if "low" in urgency_str else TaskPriority.MEDIUM)
            unresolved.append(
                UnresolvedIssue(
                    issue=_find_key(u, "issue", "blocker", "title") or "",
                    context=_find_key(u, "context", "description"),
                    urgency=urgency,
                    timestamp=_parse_timestamp(_find_key(u, "timestamp", "time"))
                )
            )

        # 11. Parse Follow-up Items
        follow_ups: List[FollowUpItem] = []
        raw_followups = _find_key(raw_result, "follow_ups", "FollowUpItems", "follow_up_items") or []
        for f in raw_followups:
            if not isinstance(f, dict):
                continue
            follow_ups.append(
                FollowUpItem(
                    item=_find_key(f, "item", "action", "title") or "",
                    suggested_owner=_find_key(f, "suggested_owner", "owner"),
                    suggested_timeframe=_find_key(f, "suggested_timeframe", "timeframe", "when")
                )
            )

        # 12. Parse Sentiment
        raw_sentiment = _find_key(raw_result, "sentiment", "SentimentTeamDynamics", "sentiment_team_dynamics") or {}
        overall_str = str(_find_key(raw_sentiment, "overall_sentiment", "overall", "sentiment") or "neutral").lower()
        if "pos" in overall_str:
            overall_cat = SentimentCategory.POSITIVE
        elif "neg" in overall_str:
            overall_cat = SentimentCategory.NEGATIVE
        elif "mix" in overall_str:
            overall_cat = SentimentCategory.MIXED
        else:
            overall_cat = SentimentCategory.NEUTRAL

        sentiment = SentimentAnalysis(
            overall_sentiment=overall_cat,
            score=float(_find_key(raw_sentiment, "score") or 0.0),
            positive_percentage=float(_find_key(raw_sentiment, "positive_percentage") or 0.0),
            neutral_percentage=float(_find_key(raw_sentiment, "neutral_percentage") or 100.0),
            negative_percentage=float(_find_key(raw_sentiment, "negative_percentage") or 0.0),
            tone_summary=str(_find_key(raw_sentiment, "tone_summary", "tone") or "")
        )

        # 13. Summaries
        exec_summary = _stringify_summary(
            _find_key(raw_result, "executive_summary", "ExecutiveSummary", "summary"),
            default="No executive summary generated."
        )
        det_summary = _stringify_summary(
            _find_key(raw_result, "detailed_summary", "DetailedSummary"),
            default="No detailed summary generated."
        )

        summary = MeetingSummary(
            executive_summary=exec_summary,
            detailed_summary=det_summary,
            summary_type_provided=request.summary_type
        )

        elapsed = round(time.time() - start_time, 3)

        metadata = MeetingMetadata(
            total_duration_seconds=request.duration,
            total_segments=len(request.segments),
            word_count=word_count,
            language=request.language,
            model_name=self.provider.model_name,
            processing_time_seconds=elapsed,
            chunk_count=chunk_count
        )

        title = raw_result.get("title") or request.meeting_title or "Executive Meeting Summary"

        return MeetingIntelligenceReport(
            title=title,
            summary=summary,
            participants=base_participants,
            key_points=key_points,
            decisions=decisions,
            action_items=action_items,
            deadlines=deadlines,
            unresolved_issues=unresolved,
            follow_ups=follow_ups,
            sentiment=sentiment,
            metadata=metadata
        )
