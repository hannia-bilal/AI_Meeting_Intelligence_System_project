"""
Standalone FastAPI microservice for AI Meeting Intelligence.
Author: Muhammad Awais (AI Meeting Intelligence)

Provides REST endpoints for:
- POST /api/v1/intelligence/analyze: Full meeting analysis
- POST /api/v1/intelligence/db-payload: Analysis + formatted DB records for PostgreSQL
- GET /health: Health check and provider status
- GET /schema: Complete OpenAPI / JSON schema for Frontend and DB teams
"""

import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure local src is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai_intelligence.schemas import (
    MeetingAnalysisRequest,
    MeetingIntelligenceReport,
    MeetingQARequest,
    MeetingQAAnswer,
    TranscriptSegment
)
from src.ai_intelligence.service import MeetingIntelligenceService

load_dotenv()

app = FastAPI(
    title="AI Meeting Intelligence API",
    description="Transforms speech transcripts into structured business intelligence (Summaries, Decisions, Actions, Deadlines, Sentiment). Built by Muhammad Awais.",
    version="1.0.0"
)

# Enable CORS for Ali Zafar's Next.js / React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default service instance
service = MeetingIntelligenceService()


@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint returning active configuration and LLM provider.
    """
    return {
        "status": "healthy",
        "module": "AI Meeting Intelligence",
        "author": "Muhammad Awais",
        "active_provider_model": service._provider.model_name
    }


@app.post(
    "/api/v1/intelligence/analyze",
    response_model=MeetingIntelligenceReport,
    tags=["Intelligence"],
    summary="Analyze Meeting Transcript"
)
async def analyze_meeting_endpoint(
    request: MeetingAnalysisRequest,
    provider: Optional[str] = Query(None, description="Optional override: 'mock', 'gemini', or 'openai'")
):
    """
    Primary API endpoint invoked by backend/processing pipeline (Faez Ahmad).
    Accepts speech segments and returns comprehensive meeting intelligence report.
    """
    try:
        active_service = service
        if provider:
            active_service = MeetingIntelligenceService(provider_type=provider)
        report = await active_service.analyze_meeting(request)
        return report
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)}")


@app.post(
    "/api/v1/intelligence/db-payload",
    tags=["Database Integration"],
    summary="Generate PostgreSQL Formatted Records"
)
async def generate_db_payload_endpoint(
    request: MeetingAnalysisRequest,
    meeting_id: Optional[str] = Query(None, description="Associated database meeting UUID/ID"),
    provider: Optional[str] = Query(None, description="Optional override: 'mock', 'gemini', 'openai', or 'groq'")
):
    """
    Convenience endpoint for Hassan Raza (Database) to receive data
    pre-structured for PostgreSQL relational tables (meetings, action_items, decisions, etc.).
    """
    try:
        active_service = service
        if provider:
            active_service = MeetingIntelligenceService(provider_type=provider)
        report = await active_service.analyze_meeting(request)
        db_records = active_service.to_database_records(report, meeting_id=meeting_id)
        return {
            "status": "success",
            "report": report,
            "database_records": db_records
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database payload generation failed: {str(exc)}")


@app.post(
    "/api/v1/intelligence/ask",
    response_model=MeetingQAAnswer,
    tags=["Meeting Q&A"],
    summary="Ask Question About Meeting (Ask AI with Timestamps)"
)
async def ask_meeting_endpoint(
    request: MeetingQARequest,
    provider: Optional[str] = Query(None, description="Optional override: 'mock', 'gemini', 'openai', or 'groq'")
):
    """
    Contextual Q&A endpoint ('Ask AI') fulfilling PDF page 4 & 5 requirement:
    Users ask questions about the meeting and receive answers with clickable timestamp references.
    """
    try:
        active_service = service
        if provider:
            active_service = MeetingIntelligenceService(provider_type=provider)

        # Default sample transcript if none passed
        segments = []
        if request.transcript_text:
            segments = [TranscriptSegment(speaker="SPEAKER", start=0.0, end=10.0, text=request.transcript_text)]
        else:
            # Load default fixture for quick testing if empty
            sample_path = Path(__file__).parent.parent / "tests" / "fixtures" / "sample_taskeen_transcript.json"
            if sample_path.exists():
                import json
                with open(sample_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    segments = [TranscriptSegment(**s) for s in data.get("segments", [])]

        answer = await active_service.ask_question(
            segments=segments,
            question=request.question,
            meeting_title=request.meeting_title
        )
        return answer
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Q&A failed: {str(exc)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("standalone_demo_api:app", host="0.0.0.0", port=8000, reload=True)
