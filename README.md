# AI Meeting Intelligence System

This project is an end-to-end AI-powered meeting intelligence platform that converts meeting audio/video into structured business insights, including summaries, key points, decisions, action items, deadlines, and contextual Q&A.

The system is designed to combine:
- speech processing
- AI analysis
- database storage
- vector search
- FastAPI backend
- React frontend

---

## Project overview

The application allows users to:
- upload audio/video files
- process meeting recordings
- generate speaker-aware transcripts
- analyze meeting content with AI
- extract decisions, action items, and deadlines
- ask questions about a meeting using contextual chat
- view results through a web dashboard and meeting details pages

---

## Tech stack

Frontend
- React + Vite
- Tailwind CSS

Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL + pgvector

AI / Processing
- Whisper-style transcription pipeline
- speaker diarization
- AI meeting analysis
- local vector embeddings + retrieval

---

## Folder structure

```text
AI_Meeting_Intelligence_System_project/
├── api/
├── Frontend/
├── src/
├── app/
├── README.md
├── requirements.txt
├── main.py
├── routes.py
├── schemas.py
├── database.py
├── config.py
├── models.py
├── qa_service.py
├── chunking.py
├── embeddings.py
├── vector_search.py
├── llm_service.py
├── test_qa_service.py
├── tests/
└── ai 19 august.pdf
```

---

## 1) Prerequisites

Install:
- Python 3.10+
- Node.js 18+
- npm
- PostgreSQL (if you want the database-backed version)

---

## 2) Backend setup

Open PowerShell in the project root:

```powershell
cd "D:\Internship\Code Celix\AI_Intelligence_Meeting\AI_Meeting_Intelligence_System_project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then start the backend:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend docs:
- http://localhost:8000/docs

Health check:
- http://localhost:8000/health

---

## 3) Frontend setup

Open a second terminal and run:

```powershell
cd "D:\Internship\Code Celix\AI_Intelligence_Meeting\AI_Meeting_Intelligence_System_project\Frontend"
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Then open:
- http://localhost:5173

---

## 4) Run the full project

To run the complete application locally:

1. Start the backend in one terminal.
2. Start the frontend in another terminal.
3. Open the frontend URL in the browser.
4. Use the app to upload or simulate a meeting and test the AI workflow.

---

## 5) Run tests

From the project root:

```powershell
pytest -q test_qa_service.py tests/test_api.py
```

This verifies the backend Q&A and API functionality.

---

## 6) Notes

- The backend supports local demo behavior even without a paid AI key.
- The project is structured so the FastAPI backend can connect with the frontend, AI service, database, and processing modules.
- If you want a full database-backed setup, configure PostgreSQL and set the appropriate environment variables.

---

## 7) Backend integration role

This project includes the backend and integration layer responsible for:
- FastAPI APIs
- frontend-to-AI communication
- database connection and persistence
- processing pipeline orchestration
- structured meeting intelligence delivery

This is the core integration point connecting all modules into one working system.
