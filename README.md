# Meeting Q&A + Vector Search
**Owner:** Absar Akbar — AI Meeting Intelligence System (Project 4)

This module implements the **"Ask AI"** feature from the spec: a contextual
chat that answers questions about one specific meeting, grounded in that
meeting's transcript, with clickable timestamp references back to the
recording.

## How it works (pipeline)

```
Taskeen's transcript segments (speaker + text + timestamps)
        ↓
chunking.py      → groups segments into coherent, timestamped chunks
        ↓
embeddings.py    → embeds each chunk (local model, no API key needed)
        ↓
vector_search.py → stores embeddings in Postgres/pgvector, does similarity search
        ↓
llm_service.py   → sends top-matching chunks + question to Claude, gets a
                    grounded answer + which excerpts it used
        ↓
qa_service.py    → maps used excerpts back to real timestamps, logs the
                    conversation, returns the final answer
        ↓
routes.py        → exposes it all as two REST endpoints
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/meetings/{meeting_id}/index` | Index a meeting's transcript for search (call once transcription finishes) |
| POST | `/meetings/{meeting_id}/ask` | Ask a question about that meeting, get an answer + timestamps |

Example `ask` request:
```json
{
  "meeting_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "question": "What did we decide about the marketing budget?"
}
```

Example response:
```json
{
  "answer": "The marketing budget was finalized at $5000.",
  "timestamp_references": [
    {"start_time_seconds": 1960, "end_time_seconds": 1970, "speaker": "Speaker 1", "snippet": "We decided the marketing budget is finalized..."}
  ]
}
```
The frontend (Ali) can use `start_time_seconds` to jump the video/audio
player to that point — exactly what spec section 8 asks for.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL and ANTHROPIC_API_KEY
uvicorn app.main:app --reload
# Swagger docs: http://localhost:8000/docs
```

Without an `ANTHROPIC_API_KEY` set, `/ask` still works — it falls back to
returning the most relevant transcript excerpt directly, so you can demo
retrieval even before wiring up the paid LLM call.

## Integration points with the rest of the team

- **Hassan (Database):** `meeting_chunks` and `qa_conversations` (see
  `schema.sql`) are new tables that reference his existing `meetings` and
  `users` tables. Run his migrations first, then this module's.
- **Taskeen (Speech Processing):** whatever her pipeline outputs for
  speaker-wise transcript + timestamps should map directly into
  `TranscriptSegmentIn` (see `app/schemas.py`) — call `/index` with that
  right after transcription finishes.
- **Awais (LLM Analysis):** his summary/decisions/action-items work is
  separate from this module (that's meeting-level analysis run once); this
  module is for interactive follow-up questions. No overlap, but both use
  an LLM — worth agreeing on one shared Anthropic client/config if he's also
  calling Claude, to avoid two separate configs.
- **Faez (Backend & Integration):** mount `app/routes.py`'s router into the
  main FastAPI app with `app.include_router(qa_router)`. Auth is stubbed —
  wire in his auth dependency where `user_id` is used.
- **Ali (Frontend):** the "Ask AI" chat box on the Meeting Details page
  calls `/ask` and should render `timestamp_references` as clickable chips
  that seek the player to `start_time_seconds`.

## Testing

```bash
pytest tests/
```
Covers chunking logic without requiring a live database or API key — good
for a quick check before the demo.

## Notes / things to double check before merging

- `meeting_id` type here is `UUID` — confirm this matches Hassan's actual
  primary key type in the `meetings` table (change in `models.py` if he's
  using integer IDs instead).
- The pgvector `ivfflat` index in `schema.sql` is commented out — only add
  it once there's real chunk data to build the index on (per pgvector docs).
- `EMBEDDING_DIM=384` matches `all-MiniLM-L6-v2`. If you switch embedding
  models later, update this **and** the column definition in `schema.sql`
  together, or search will break silently.
