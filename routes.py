"""
API routes for Meeting Q&A + Vector Search.

Faez includes this router in the main app, e.g.:

    from app.routes import router as qa_router
    app.include_router(qa_router)

Auth: these endpoints assume request.state.user (or similar) is already
populated by Faez's auth middleware. Wire `current_user_id` accordingly —
left as a stub dependency here so this module can be developed/tested
independently.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    IndexMeetingRequest,
    IndexMeetingResponse,
    AskRequest,
    AskResponse,
)
from app.qa_service import index_meeting_transcript, ask_meeting_question

router = APIRouter(prefix="/meetings", tags=["Meeting Q&A"])


@router.post("/{meeting_id}/index", response_model=IndexMeetingResponse)
def index_meeting(meeting_id: uuid.UUID, payload: IndexMeetingRequest, db: Session = Depends(get_db)):
    if meeting_id != payload.meeting_id:
        raise HTTPException(status_code=400, detail="meeting_id in path and body must match")
    if not payload.segments:
        raise HTTPException(status_code=400, detail="No transcript segments provided")

    return index_meeting_transcript(db, meeting_id, payload.segments)


@router.post("/{meeting_id}/ask", response_model=AskResponse)
def ask_meeting(meeting_id: uuid.UUID, payload: AskRequest, db: Session = Depends(get_db)):
    if meeting_id != payload.meeting_id:
        raise HTTPException(status_code=400, detail="meeting_id in path and body must match")
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    return ask_meeting_question(db, meeting_id, payload.question, payload.user_id)
