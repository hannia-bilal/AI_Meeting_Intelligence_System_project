"""
Standalone entry point so this module can be run and tested on its own,
before Faez wires it into the main team backend.

Run: uvicorn app.main:app --reload
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI

from app.database import Base, engine, init_vector_extension
from app.routes import router as qa_router

app = FastAPI(title="Meeting Q&A + Vector Search")


@app.on_event("startup")
def startup():
    init_vector_extension()
    Base.metadata.create_all(bind=engine)


app.include_router(qa_router)


@app.get("/health")
def health():
    return {"status": "ok", "module": "meeting-qa-vector-search"}
