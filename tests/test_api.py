"""
API endpoint tests for standalone_demo_api.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

import json
from pathlib import Path
from fastapi.testclient import TestClient

from api.standalone_demo_api import app

client = TestClient(app)
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["author"] == "Muhammad Awais"


def test_api_analyze_endpoint():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

    res = client.post("/api/v1/intelligence/analyze?provider=mock", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "title" in data
    assert "summary" in data
    assert "action_items" in data
    assert "decisions" in data
    assert "participants" in data
    assert len(data["action_items"]) > 0


def test_api_db_payload_endpoint():
    with open(FIXTURES_DIR / "sample_taskeen_transcript.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

    res = client.post("/api/v1/intelligence/db-payload?meeting_id=meet_abc&provider=mock", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["database_records"]["meeting_id"] == "meet_abc"
    assert "meeting_updates" in data["database_records"]
