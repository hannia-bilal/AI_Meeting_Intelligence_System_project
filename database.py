"""
Database engine/session setup.

Uses the SAME PostgreSQL database as the rest of the team (Hassan's schema
for users/meetings/transcripts/etc). This module only adds the tables it
owns: meeting_chunks (for vector search) and qa_conversations (chat log).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_vector_extension():
    """
    Ensures the pgvector extension is enabled on the shared Postgres DB.
    Safe to call multiple times (IF NOT EXISTS).
    Call this once at app startup, after Hassan's core schema is migrated.
    """
    with engine.connect() as conn:
        conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()
