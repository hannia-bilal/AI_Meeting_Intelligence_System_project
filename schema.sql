-- Tables owned by the Meeting Q&A + Vector Search module.
-- Run AFTER Hassan's core schema (users, meetings, transcripts, etc.)
-- since meeting_id here references his meetings table.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS meeting_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    speaker VARCHAR(120),
    text TEXT NOT NULL,
    start_time_seconds FLOAT NOT NULL,
    end_time_seconds FLOAT NOT NULL,
    embedding VECTOR(384) NOT NULL,   -- 384 = all-MiniLM-L6-v2 dimension
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_meeting_chunks_meeting_id ON meeting_chunks (meeting_id);

-- IVFFlat index for fast approximate cosine search once you have enough rows
-- (run ANALYZE meeting_chunks; after populating data, then create this):
-- CREATE INDEX idx_meeting_chunks_embedding ON meeting_chunks
--   USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE IF NOT EXISTS qa_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    cited_timestamps TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_qa_conversations_meeting_id ON qa_conversations (meeting_id);
