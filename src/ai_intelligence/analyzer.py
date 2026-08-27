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
        for mapping in raw_result.get("speaker_name_mappings", []):
            spk_id = mapping.get("speaker_id")
            name = mapping.get("detected_name")
            if spk_id and name:
                name_map[spk_id] = name

        for p in base_participants:
            if p.speaker_id in name_map:
                p.detected_name = name_map[p.speaker_id]

        # 6. Parse and normalize Action Items & Deadlines
        action_items: List[ActionItem] = []
        for item in raw_result.get("action_items", []):
            raw_deadline = item.get("deadline_raw")
            norm_deadline = normalize_deadline(raw_deadline, request.meeting_date)
            ts = _parse_timestamp(item.get("timestamp"))

            # Determine priority enum
            priority_str = (item.get("priority") or "medium").lower()
            priority = TaskPriority.MEDIUM
            if "high" in priority_str:
                priority = TaskPriority.HIGH
            elif "low" in priority_str:
                priority = TaskPriority.LOW

            action_items.append(
                ActionItem(
                    task=item.get("task", "Untitled Task"),
                    assigned_to=item.get("assigned_to", "Unassigned"),
                    assigned_speaker_id=item.get("assigned_speaker_id"),
                    deadline_raw=raw_deadline,
                    deadline_normalized=norm_deadline,
                    priority=priority,
                    status=TaskStatus.PENDING,
                    timestamp=ts
                )
            )

        # 7. Parse Deadlines
        deadlines: List[DeadlineItem] = []
        for d in raw_result.get("deadlines", []):
            raw_text = d.get("raw_text", "")
            norm_date = normalize_deadline(raw_text, request.meeting_date)
            deadlines.append(
                DeadlineItem(
                    item=d.get("item", "Milestone"),
                    raw_text=raw_text,
                    normalized_date=norm_date,
                    context=d.get("context")
                )
            )

        # 8. Parse Key Points
        key_points: List[KeyDiscussionPoint] = []
        for kp in raw_result.get("key_points", []):
            key_points.append(
                KeyDiscussionPoint(
                    topic=kp.get("topic", "Discussion Point"),
                    summary=kp.get("summary", ""),
                    timestamp=_parse_timestamp(kp.get("timestamp")),
                    speaker=kp.get("speaker")
                )
            )

        # 9. Parse Decisions
        decisions: List[DecisionItem] = []
        for dec in raw_result.get("decisions", []):
            decisions.append(
                DecisionItem(
                    decision=dec.get("decision", ""),
                    rationale=dec.get("rationale"),
                    timestamp=_parse_timestamp(dec.get("timestamp")),
                    agreed_by=dec.get("agreed_by", [])
                )
            )

        # 10. Parse Unresolved Issues
        unresolved: List[UnresolvedIssue] = []
        for u in raw_result.get("unresolved_issues", []):
            urgency_str = (u.get("urgency") or "medium").lower()
            urgency = TaskPriority.HIGH if "high" in urgency_str else (TaskPriority.LOW if "low" in urgency_str else TaskPriority.MEDIUM)
            unresolved.append(
                UnresolvedIssue(
                    issue=u.get("issue", ""),
                    context=u.get("context"),
                    urgency=urgency,
                    timestamp=_parse_timestamp(u.get("timestamp"))
                )
            )

        # 11. Parse Follow-up Items
        follow_ups: List[FollowUpItem] = []
        for f in raw_result.get("follow_ups", []):
            follow_ups.append(
                FollowUpItem(
                    item=f.get("item", ""),
                    suggested_owner=f.get("suggested_owner"),
                    suggested_timeframe=f.get("suggested_timeframe")
                )
            )

        # 12. Parse Sentiment
        raw_sentiment = raw_result.get("sentiment", {})
        overall_str = (raw_sentiment.get("overall_sentiment") or "neutral").lower()
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
            score=float(raw_sentiment.get("score", 0.0)),
            positive_percentage=float(raw_sentiment.get("positive_percentage", 0.0)),
            neutral_percentage=float(raw_sentiment.get("neutral_percentage", 100.0)),
            negative_percentage=float(raw_sentiment.get("negative_percentage", 0.0)),
            tone_summary=raw_sentiment.get("tone_summary", "")
        )

        # 13. Summaries
        summary = MeetingSummary(
            executive_summary=raw_result.get("executive_summary", "No executive summary generated."),
            detailed_summary=raw_result.get("detailed_summary", "No detailed summary generated."),
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
