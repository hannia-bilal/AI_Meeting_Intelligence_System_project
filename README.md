# AI Meeting Intelligence System

An AI-powered web application that turns meeting audio and video into structured, actionable business intelligence. Instead of producing only a transcript, the system identifies what was discussed, what was decided, who owns each task, when work is due, and what still needs attention.

## Project Objectives

- Upload audio and video meeting recordings.
- Optionally record a meeting in the browser.
- Generate an intelligent meeting report from each recording.
- Preserve timestamps and identify speakers where possible.
- Support contextual questions about a selected meeting.
- Provide a responsive dashboard for meeting history and follow-up work.

## AI-Generated Meeting Report

Each processed meeting can include:

- Automatically generated title
- Short or detailed executive summary
- Detailed summary and key discussion points
- Participants and speaker-wise transcript
- Decisions made during the meeting
- Action items, task owners, and deadlines
- Unresolved issues and follow-up items
- Overall meeting sentiment

Natural-language deadlines such as “tomorrow”, “Friday”, “next Monday”, “September 10”, and “end of this month” are normalized into structured dates where possible.

## Core Features

### Speech Processing

- Common audio and video format support
- Speech-to-text using Whisper or an equivalent model
- Timestamp preservation
- Speaker identification and diarization where possible
- Background processing for long recordings

### AI Analysis

The analysis pipeline extracts summaries, key points, decisions, action items, owners, deadlines, unresolved issues, follow-ups, and sentiment from the transcript. Users can choose between short and detailed summaries.

### Meeting Q&A

Ask questions about the currently selected meeting, such as “What did we decide about the marketing budget?” Answers use only that meeting’s transcript and structured insights, and include relevant timestamp references. Selecting a timestamp takes the user to that point in the recording.

### Dashboard

The dashboard provides:

- Recent meetings
- Processing status
- Meeting duration
- Action-item count
- Pending decisions
- Upcoming deadlines
- Meeting search

### Meeting Details

Each meeting has overview, transcript, AI insights, and Ask AI views. The transcript supports speaker labels, timestamps, and search. AI insights display key points, decisions, action items, deadlines, and unresolved issues.

## System Architecture

```text
Audio / Video / Browser Recording
		    |
		    v
	 Speech-to-Text Processing
		    |
		    v
	 Speaker Identification
		    |
		    v
	    Transcript Storage
		    |
		    v
	     LLM Analysis
		    |
		    v
 Structured Meeting Intelligence
		    |
		    v
	 Embeddings + pgvector
		    |
		    v
	  Contextual Meeting Q&A
```

## Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | React or Next.js with TypeScript |
| Backend | Python with FastAPI |
| Database | PostgreSQL with pgvector |
| Speech-to-text | Whisper or equivalent |
| LLM analysis | OpenAI, Gemini, Claude, or an equivalent provider |
| Storage | S3-compatible object storage |
| Processing | Background workers for large files |
| API style | REST with documented request and response schemas |

## Backend API Scope

The backend will expose APIs for:

- User authentication, authorization, and profile management
- Secure meeting file upload and file management
- Audio/video processing and processing-status updates
- Transcription and speaker data
- Meeting summaries and AI insights
- Action items, decisions, deadlines, and follow-ups
- Contextual meeting Q&A with timestamp references
- Meeting search and meeting history

All endpoints should validate inputs, enforce authorization, handle failures consistently, and avoid exposing secrets or unauthorized meeting data.

## Data Model

The PostgreSQL schema should support the following entities and relationships:

- `users`
- `meetings`
- `participants`
- `speakers`
- `transcripts`
- `action_items`
- `decisions`
- `deadlines`
- `ai_conversations`
- `files`

Indexes should support meeting history, transcript search, processing status, deadlines, and vector similarity queries.

## Team Responsibilities

| Member | Main role | Primary deliverable | Secondary responsibility |
| --- | --- | --- | --- |
| Muhammad Awais | AI Meeting Intelligence | LLM analysis for summaries, key points, decisions, action items, owners, deadlines, unresolved issues, follow-ups, and sentiment | AI prompt and response structure |
| Faez Ahmad | Backend & Integration | FastAPI backend and integration of frontend, AI, database, and processing modules | Overall module integration |
| Taskeen Mustafa | Speech Processing | Audio/video processing, speech-to-text, timestamps, speaker identification, and transcript generation | Long-recording support |
| Ali Zafar | Database & Meeting Management | PostgreSQL schema for users, meetings, participants, transcripts, speakers, insights, and files | Meeting history and search APIs |
| Hassan Raza | Frontend & Dashboard | React/Next.js upload flow, dashboard, meeting details, transcript viewer, and AI insights | Responsive UI |
| Absar Akbar | Meeting Q&A & Vector Search | Ask AI using transcript and structured data, embeddings, vector search, contextual answers, and timestamp references | Module QA and final system testing |

## Engineering Requirements

- Clean architecture with reusable components
- Secure file uploads and S3-compatible storage
- Authentication and meeting-level authorization
- Input validation and consistent error handling
- Background processing for large recordings
- Database indexes for frequent queries and vector search
- Environment variables for API keys and other secrets
- REST API documentation
- Responsive web interface
- Git-based collaboration and version control

## Local Setup

The repository is currently being organized around the frontend, FastAPI backend, processing workers, and database services. Once those modules are added, setup should follow these steps:

1. Clone the repository and create the required frontend and backend environments.
2. Configure environment variables for PostgreSQL, object storage, speech-to-text, LLM, and embedding providers.
3. Start PostgreSQL with the `pgvector` extension and apply the database migrations.
4. Install frontend and backend dependencies.
5. Start the FastAPI service, background worker, and frontend development server.
6. Open the frontend and upload a meeting recording to begin processing.

Never commit credentials, uploaded recordings, generated transcripts, or other sensitive meeting data.

## AI Meeting Intelligence Module (Muhammad Awais)

This module implements the complete **AI Meeting Intelligence Engine** and **AI Prompt Response Architecture** built by **Muhammad Awais**.

It takes raw, diarized speech transcripts (from Taskeen Mustafa) and extracts:
- **Executive & Detailed Summaries** (supporting short, detailed, or dual summaries)
- **Speaker Mapping & Contribution Metrics** (speaking time, contribution percentage, turn counts, mapping `SPEAKER_XX` to real names)
- **Key Discussion Points** with timestamp references (`MM:SS`)
- **Decisions Made** with rationale and timestamps
- **Action Items & Task Owners** with natural deadline detection and ISO-8601 normalization (e.g., "Friday" -> `2026-09-04`, "next Monday" -> `2026-08-31`, "September 10" -> `2026-09-10`, "end of this month" -> `2026-08-31`)
- **Deadlines & Milestones**
- **Unresolved Issues & Blockers** with urgency ratings
- **Follow-up Items** with recommended owners and timeframes
- **Overall Meeting Sentiment & Dynamics** (sentiment score `-1.0` to `+1.0`, category, and qualitative tone summary)

### Module Architecture

```text
src/ai_intelligence/
├── __init__.py           # Package exports
├── schemas.py            # Strict Pydantic models (Input & Output contracts)
├── normalizers.py        # Date/deadline normalizer & timestamp utilities
├── chunker.py            # Long meeting transcript chunking & speaker metrics
├── prompts.py            # Structured system & user prompts + JSON schema
├── analyzer.py           # Core MeetingIntelligenceAnalyzer orchestrator
├── service.py            # High-level facade for FastAPI & Database integration
└── providers/            # Multi-LLM provider abstraction
    ├── base.py           # BaseLLMProvider interface
    ├── mock_provider.py  # High-fidelity offline mock for testing without API keys
    ├── gemini_provider.py# Google Gemini API integration (gemini-1.5-flash)
    └── openai_provider.py# OpenAI API integration (gpt-4o-mini)
```

### Team Integration Guide

#### 1. For Faez Ahmad (Backend & Integration)
Import `MeetingIntelligenceService` in your FastAPI router:
```python
from src.ai_intelligence.service import MeetingIntelligenceService

service = MeetingIntelligenceService(provider_type="gemini") # or "openai" or "mock"

@router.post("/api/v1/meetings/{meeting_id}/analyze")
async def analyze_meeting(meeting_id: str, transcript_data: dict):
    # Non-blocking async execution
    report = await service.analyze_meeting(transcript_data)
    return report
```

#### 2. For Taskeen Mustafa (Speech Processing)
Output your Whisper/Diarization results in this JSON contract (approved in WhatsApp):
```json
{
  "duration": 1845.0,
  "language": "en",
  "meeting_title": "Optional Title",
  "meeting_date": "2026-08-28T10:00:00Z",
  "segments": [
    {
      "speaker": "SPEAKER_00",
      "start": 135.2,
      "end": 141.8,
      "text": "We should launch the website next week."
    }
  ]
}
```

#### 3. For Hassan Raza (Database & Meeting Management)
Use `service.to_database_records(report, meeting_id)` to get pre-mapped dictionaries ready for PostgreSQL insertion:
```python
db_payload = MeetingIntelligenceService.to_database_records(report, meeting_id=meeting.id)
# Contains:
# - db_payload["meeting_updates"] -> title, summaries, sentiment
# - db_payload["action_items"] -> tasks, assignees, normalized deadlines, priorities
# - db_payload["decisions"] -> decisions, rationale, timestamps
# - db_payload["participants"] -> speaker metrics, detected names
```

#### 4. For Absar Akbar (Meeting Q&A + Vector Search)
Use the structured `report.key_points`, `report.decisions`, and `report.action_items` along with `TimestampReference` (`seconds`, `formatted`) for indexing into `pgvector` chunks.

#### 5. For Ali Zafar (Frontend & Dashboard)
The API returns a fully typed JSON object matching the `MeetingDetailsPage` requirements in the specification:
- Overview (Summary, Participants, Duration, Date)
- Transcript (Speaker labels, Timestamps, Searchable)
- AI Insights (Key points, Decisions, Action Items, Deadlines, Unresolved Issues)

---

### Running the Module

#### 1. Run Automated Test Suite
```bash
python -m pytest tests/ -v
```

#### 2. Run via CLI
```bash
python cli.py --input tests/fixtures/sample_taskeen_transcript.json --provider mock --output report.json
```

#### 3. Run Standalone FastAPI Microservice & Swagger UI
```bash
python api/standalone_demo_api.py
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## Deliverables

- Complete source code
- Functional responsive web application
- FastAPI backend APIs
- PostgreSQL and pgvector schema
- Speech processing and AI integration
- API documentation
- Setup instructions
- Demonstration video

## Project Timeline

- Duration: 2 weeks
- Submission deadline: 1 week, 4:00 PM