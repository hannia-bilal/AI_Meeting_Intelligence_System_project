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