"""
High-level Meeting Intelligence Service.
Author: Muhammad Awais (AI Meeting Intelligence)

Integration facade for Faez Ahmad (FastAPI backend), Hassan Raza (PostgreSQL schema),
Absar Akbar (Vector Q&A), and Ali Zafar (Frontend).
"""

import asyncio
from typing import Optional, Dict, Any
from .schemas import MeetingAnalysisRequest, MeetingIntelligenceReport
from .providers import get_llm_provider, BaseLLMProvider
from .analyzer import MeetingIntelligenceAnalyzer


class MeetingIntelligenceService:
    """
    Primary service entrypoint for the AI Meeting Intelligence module.
    """

    def __init__(
        self,
        provider: Optional[BaseLLMProvider] = None,
        provider_type: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        if provider:
            self._provider = provider
        else:
            self._provider = get_llm_provider(
                provider_type=provider_type,
                api_key=api_key,
                model_name=model_name
            )
        self._analyzer = MeetingIntelligenceAnalyzer(provider=self._provider)

    def analyze_meeting_sync(self, request_data: Any) -> MeetingIntelligenceReport:
        """
        Synchronously analyzes a meeting transcript payload.
        Accepts either a dict or a validated MeetingAnalysisRequest.
        """
        if isinstance(request_data, dict):
            req = MeetingAnalysisRequest(**request_data)
        elif isinstance(request_data, MeetingAnalysisRequest):
            req = request_data
        else:
            raise ValueError(f"Expected dict or MeetingAnalysisRequest, got {type(request_data)}")

        return self._analyzer.analyze(req)

    async def analyze_meeting(self, request_data: Any) -> MeetingIntelligenceReport:
        """
        Asynchronous wrapper designed for non-blocking execution in FastAPI routes.
        Offloads LLM call to threadpool.
        """
        return await asyncio.to_thread(self.analyze_meeting_sync, request_data)

    def ask_question_sync(
        self,
        segments: Any,
        question: str,
        meeting_title: Optional[str] = None
    ):
        """
        Answers a user question about a meeting with timestamp references (Ask AI).
        Accepts a list of TranscriptSegment or list of dicts.
        """
        from .schemas import TranscriptSegment
        parsed_segments = []
        for s in segments:
            if isinstance(s, dict):
                parsed_segments.append(TranscriptSegment(**s))
            else:
                parsed_segments.append(s)
        return self._analyzer.answer_question(parsed_segments, question, meeting_title)

    async def ask_question(
        self,
        segments: Any,
        question: str,
        meeting_title: Optional[str] = None
    ):
        """
        Asynchronous wrapper for Ask AI feature.
        """
        return await asyncio.to_thread(self.ask_question_sync, segments, question, meeting_title)

    @staticmethod
    def to_database_records(report: MeetingIntelligenceReport, meeting_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Helper method specifically provided for Hassan Raza (Database & Meeting Management)
        to map structured AI intelligence into relational tables:
        - meetings (title, summary, sentiment, score, duration)
        - action_items (task, assigned_to, deadline_normalized, priority, status)
        - decisions (decision, rationale, timestamp)
        - deadlines (item, raw_text, normalized_date)
        - participants (speaker_id, detected_name, contribution_percentage)
        - transcripts (speaker-wise segments with formatted timestamps)
        - dashboard_metrics (pre-calculated metrics for fast querying)
        """
        return {
            "meeting_id": meeting_id,
            "meeting_updates": {
                "title": report.title,
                "executive_summary": report.summary.executive_summary,
                "detailed_summary": report.summary.detailed_summary,
                "sentiment": report.sentiment.overall_sentiment.value,
                "sentiment_score": report.sentiment.score,
                "tone_notes": report.sentiment.tone_summary,
            },
            "participants": [p.model_dump() for p in report.participants],
            "speaker_wise_transcript": [s.model_dump() for s in report.speaker_wise_transcript],
            "action_items": [a.model_dump() for a in report.action_items],
            "decisions": [d.model_dump() for d in report.decisions],
            "deadlines": [dl.model_dump() for dl in report.deadlines],
            "key_points": [kp.model_dump() for kp in report.key_points],
            "unresolved_issues": [u.model_dump() for u in report.unresolved_issues],
            "follow_ups": [f.model_dump() for f in report.follow_ups],
            "dashboard_metrics": report.dashboard_metrics.model_dump() if report.dashboard_metrics else None,
        }
