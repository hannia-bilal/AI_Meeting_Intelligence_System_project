"""
High-fidelity offline Mock LLM Provider for testing and local development.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import re
from typing import Dict, Any, Optional
from .base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """
    Offline mock provider that produces realistic structured JSON reports
    tailored to the supplied transcript.
    """

    def __init__(self, model_name: str = "mock-intelligence-v1"):
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Handle Meeting Q&A ("Ask AI") queries
        if "QUESTION:" in user_prompt:
            return {
                "answer": "The team decided to launch the product on September 1 and agreed to review the staging environment next Monday.",
                "relevant_timestamps": [
                    {"seconds": 149.0, "formatted": "02:29"}
                ],
                "referenced_speakers": ["SPEAKER_00", "Ali"],
                "evidence_quotes": [
                    "We decided to launch the product on September 1."
                ]
            }

        # Look for speaker cues and text
        has_launch = "launch" in user_prompt.lower()
        has_backend = "backend" in user_prompt.lower()
        has_ali = "ali" in user_prompt.lower()
        has_friday = "friday" in user_prompt.lower()

        title = "Sprint Planning & Website Launch Review" if has_launch else "Project Strategy & Technical Alignment Meeting"

        executive = (
            "The team met to coordinate critical launch deliverables, system architecture, "
            "and backend service readiness. Key ownership roles were established, and clear timelines "
            "were set for immediate delivery."
        )

        detailed = (
            "### 1. Launch Preparation & Objectives\n"
            "The team reviewed milestone requirements for the upcoming release, noting feature dependencies.\n\n"
            "### 2. Engineering & Architecture\n"
            "Technical responsibilities were distributed across backend and frontend tracks to avoid blockers.\n\n"
            "### 3. Timelines & Accountability\n"
            "Deadlines were finalized with team leads committed to passing all quality checks on schedule."
        )

        return {
            "title": title,
            "executive_summary": executive,
            "detailed_summary": detailed,
            "speaker_name_mappings": [
                {"speaker_id": "SPEAKER_00", "detected_name": "Hannia" if "hannia" in user_prompt.lower() else "Lead"},
                {"speaker_id": "SPEAKER_01", "detected_name": "Ali" if has_ali else "Engineer"}
            ],
            "key_points": [
                {
                    "topic": "Release Schedule",
                    "summary": "Targeting launch window next week following QA approval.",
                    "timestamp": "02:15",
                    "speaker": "SPEAKER_00"
                },
                {
                    "topic": "Backend Readiness",
                    "summary": "Core API endpoints and validation layers slated for completion.",
                    "timestamp": "02:22",
                    "speaker": "SPEAKER_01"
                }
            ],
            "decisions": [
                {
                    "decision": "Proceed with planned release schedule for next week.",
                    "rationale": "All prerequisite modules are on track for QA handoff.",
                    "timestamp": "02:15",
                    "agreed_by": ["SPEAKER_00", "SPEAKER_01"]
                },
                {
                    "decision": "Adopt standardized JSON schema for inter-module communication.",
                    "rationale": "Ensures seamless contract between Speech, AI, Backend, and UI.",
                    "timestamp": "02:28",
                    "agreed_by": ["SPEAKER_00", "SPEAKER_01"]
                }
            ],
            "action_items": [
                {
                    "task": "Finish backend service integration and test endpoints",
                    "assigned_to": "Ali" if has_ali else "SPEAKER_01",
                    "assigned_speaker_id": "SPEAKER_01",
                    "deadline_raw": "Friday" if has_friday else "end of this week",
                    "priority": "high",
                    "timestamp": "02:22"
                },
                {
                    "task": "Review website deployment staging checklist",
                    "assigned_to": "SPEAKER_00",
                    "assigned_speaker_id": "SPEAKER_00",
                    "deadline_raw": "next Monday",
                    "priority": "medium",
                    "timestamp": "02:15"
                }
            ],
            "deadlines": [
                {
                    "item": "Backend Completion",
                    "raw_text": "Friday" if has_friday else "end of this week",
                    "context": "Verification and integration tests handoff"
                },
                {
                    "item": "Staging Deployment Review",
                    "raw_text": "next Monday",
                    "context": "Final review prior to production rollout"
                }
            ],
            "unresolved_issues": [
                {
                    "issue": "High concurrency load testing on Speech Processing worker",
                    "context": "Need confirmation if local GPUs or cloud endpoints will handle peak transcription loads",
                    "urgency": "medium",
                    "timestamp": "02:30"
                }
            ],
            "follow_ups": [
                {
                    "item": "Verify API contracts with Frontend team",
                    "suggested_owner": "Backend Lead",
                    "suggested_timeframe": "Tomorrow morning"
                }
            ],
            "sentiment": {
                "overall_sentiment": "positive",
                "score": 0.75,
                "positive_percentage": 70.0,
                "neutral_percentage": 25.0,
                "negative_percentage": 5.0,
                "tone_summary": "Highly collaborative, constructive, and oriented toward concrete deadlines."
            }
        }
