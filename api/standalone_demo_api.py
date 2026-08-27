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

from src.ai_intelligence.schemas import MeetingAnalysisRequest, MeetingIntelligenceReport
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("standalone_demo_api:app", host="0.0.0.0", port=8000, reload=True)
