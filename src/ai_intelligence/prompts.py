"""
AI prompts and structured response templates for Meeting Intelligence.
Author: Muhammad Awais (AI Meeting Intelligence)

Enforces deterministic, structured JSON output for:
- Executive and Detailed summaries
- Speaker mapping (SPEAKER_XX -> real names if mentioned)
- Key discussion points with timestamps
- Decisions made with rationale and timestamps
- Action items, owners, deadlines, priorities, and timestamps
- Unresolved issues and blockers
- Follow-ups
- Sentiment analysis and tone breakdown
"""

import json
from typing import Dict, Any
from .schemas import SummaryType

SYSTEM_PROMPT = """You are an elite AI Meeting Intelligence Engine designed to convert unstructured multi-speaker meeting transcripts into precise, actionable business intelligence.

Your analysis must be objective, factual, and strictly grounded in the provided transcript. Do not fabricate or assume information not discussed.

You will extract:
1. Descriptive Meeting Title: Concise and representative of the main objective.
2. Executive Summary: High-level overview (1-2 paragraphs) for leadership.
3. Detailed Summary: Comprehensive breakdown organized by themes, proposals, and outcomes.
4. Speaker Name Mapping: If speakers refer to each other by name (e.g., "Ali, what do you think?", "Thanks Hassan"), correlate speaker labels (SPEAKER_00, SPEAKER_01) to their real names where clear.
5. Key Discussion Points: Major ideas or topics debated, with timestamp references.
6. Decisions Made: Explicit agreements, approvals, or strategic choices with reasoning and timestamps.
7. Action Items & Task Owners: Specific tasks assigned, the owner (person or speaker label), deadlines mentioned naturally (e.g., "Friday", "next Monday", "September 10", "end of this month"), priority (high/medium/low), and timestamps.
8. Deadlines & Milestones: Time-sensitive deliverables mentioned in conversation.
9. Unresolved Issues & Blockers: Open questions, pending approvals, or disagreements left open.
10. Follow-up Items: Required check-ins or future meeting topics.
11. Sentiment & Team Dynamics: Overall tone (positive/neutral/negative/mixed), score from -1.0 to 1.0, sentiment percentages, and qualitative tone summary.

CRITICAL INSTRUCTIONS:
- Preserve timestamps formatted as MM:SS or HH:MM:SS matching the transcript tags.
- Output MUST be valid JSON adhering exactly to the specified JSON schema.
- Do NOT wrap JSON in explanatory text outside of the JSON structure.
"""

ANALYSIS_JSON_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": [
        "title",
        "executive_summary",
        "detailed_summary",
        "speaker_name_mappings",
        "key_points",
        "decisions",
        "action_items",
        "deadlines",
        "unresolved_issues",
        "follow_ups",
        "sentiment"
    ],
    "properties": {
        "title": {"type": "string", "description": "Engaging, professional meeting title"},
        "executive_summary": {"type": "string", "description": "1-2 paragraph executive briefing"},
        "detailed_summary": {"type": "string", "description": "Detailed thematic breakdown"},
        "speaker_name_mappings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["speaker_id", "detected_name"],
                "properties": {
                    "speaker_id": {"type": "string", "description": "e.g. SPEAKER_00"},
                    "detected_name": {"type": "string", "description": "e.g. Ali, or null if unknown"}
                }
            }
        },
        "key_points": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["topic", "summary", "timestamp", "speaker"],
                "properties": {
                    "topic": {"type": "string"},
                    "summary": {"type": "string"},
                    "timestamp": {"type": "string", "description": "MM:SS format"},
                    "speaker": {"type": "string"}
                }
            }
        },
        "decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["decision", "rationale", "timestamp", "agreed_by"],
                "properties": {
                    "decision": {"type": "string"},
                    "rationale": {"type": "string"},
                    "timestamp": {"type": "string", "description": "MM:SS format"},
                    "agreed_by": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["task", "assigned_to", "deadline_raw", "priority", "timestamp"],
                "properties": {
                    "task": {"type": "string"},
                    "assigned_to": {"type": "string"},
                    "assigned_speaker_id": {"type": "string"},
                    "deadline_raw": {"type": "string", "description": "e.g. 'Friday', 'next Monday', 'September 10'"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "timestamp": {"type": "string", "description": "MM:SS format"}
                }
            }
        },
        "deadlines": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["item", "raw_text", "context"],
                "properties": {
                    "item": {"type": "string"},
                    "raw_text": {"type": "string"},
                    "context": {"type": "string"}
                }
            }
        },
        "unresolved_issues": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["issue", "context", "urgency", "timestamp"],
                "properties": {
                    "issue": {"type": "string"},
                    "context": {"type": "string"},
                    "urgency": {"type": "string", "enum": ["high", "medium", "low"]},
                    "timestamp": {"type": "string"}
                }
            }
        },
        "follow_ups": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["item", "suggested_owner", "suggested_timeframe"],
                "properties": {
                    "item": {"type": "string"},
                    "suggested_owner": {"type": "string"},
                    "suggested_timeframe": {"type": "string"}
                }
            }
        },
        "sentiment": {
            "type": "object",
            "required": [
                "overall_sentiment",
                "score",
                "positive_percentage",
                "neutral_percentage",
                "negative_percentage",
                "tone_summary"
            ],
            "properties": {
                "overall_sentiment": {"type": "string", "enum": ["positive", "neutral", "negative", "mixed"]},
                "score": {"type": "number", "minimum": -1.0, "maximum": 1.0},
                "positive_percentage": {"type": "number"},
                "neutral_percentage": {"type": "number"},
                "negative_percentage": {"type": "number"},
                "tone_summary": {"type": "string"}
            }
        }
    }
}


def build_analysis_user_prompt(
    formatted_transcript: str,
    meeting_title: str = None,
    summary_type: SummaryType = SummaryType.BOTH,
    meeting_date: str = None
) -> str:
    """
    Constructs the analysis prompt with meeting metadata and formatted transcript.
    """
    date_info = f"Meeting Reference Date: {meeting_date}\n" if meeting_date else ""
    title_info = f"Known Meeting Title/Topic: {meeting_title}\n" if meeting_title else ""
    summary_pref = f"Preferred Summary Scope: {summary_type.value}\n"

    return f"""Please analyze the following meeting transcript and produce the structured intelligence JSON report.

{title_info}{date_info}{summary_pref}
TRANSCRIPT:
---
{formatted_transcript}
---

Respond strictly with valid JSON conforming to the requested schema. Do not output markdown backticks or commentary outside the JSON.
"""
