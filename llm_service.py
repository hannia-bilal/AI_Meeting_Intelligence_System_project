"""
Calls an LLM to answer a user's question using ONLY the retrieved meeting
chunks as context (retrieval-augmented generation). This is what satisfies
spec section 7 ("Meeting Q&A") and 8 ("Timestamp References").

The model is instructed to:
  1. Answer strictly from the provided transcript excerpts.
  2. Say clearly when the meeting doesn't cover the question.
  3. Point to which excerpt(s) it used, so we can map back to timestamps
     deterministically in Python (we do NOT trust the model to invent
     timestamps — we attach the real ones ourselves from retrieval).
"""
import json
from typing import List

from anthropic import Anthropic

from app.config import settings
from app.models import MeetingChunk

_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None


def _build_context_block(chunks: List[MeetingChunk]) -> str:
    lines = []
    for i, c in enumerate(chunks):
        speaker = c.speaker or "Unknown speaker"
        lines.append(
            f"[Excerpt {i}] ({speaker}, {c.start_time_seconds:.0f}s–{c.end_time_seconds:.0f}s)\n{c.text}"
        )
    return "\n\n".join(lines)


SYSTEM_PROMPT = """You are the "Ask AI" assistant for a single meeting. \
Answer the user's question using ONLY the excerpts provided below — never use \
outside knowledge, and never invent facts, decisions, or numbers not present \
in the excerpts.

If the excerpts don't contain enough information to answer, say so plainly \
instead of guessing.

Respond with a JSON object only, no other text, in this exact shape:
{"answer": "<your answer in 1-4 sentences>", "used_excerpt_indices": [<ints>]}

"used_excerpt_indices" must list the [Excerpt N] numbers you actually relied on.
"""


def generate_answer(question: str, chunks: List[MeetingChunk]) -> dict:
    """
    Returns {"answer": str, "used_excerpt_indices": List[int]}.
    Falls back to a safe response if no LLM key is configured (e.g. local dev).
    """
    if not chunks:
        return {
            "answer": "I couldn't find anything in this meeting related to that question.",
            "used_excerpt_indices": [],
        }

    if _client is None:
        # No API key configured — return the most relevant excerpt directly
        # so the feature is still usable/demoable without a paid key.
        return {
            "answer": (
                "(LLM not configured — showing most relevant excerpt) "
                + chunks[0].text
            ),
            "used_excerpt_indices": [0],
        }

    context = _build_context_block(chunks)
    user_message = f"Excerpts:\n\n{context}\n\nQuestion: {question}"

    response = _client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    try:
        parsed = json.loads(raw_text)
        return {
            "answer": parsed.get("answer", "").strip(),
            "used_excerpt_indices": parsed.get("used_excerpt_indices", []),
        }
    except (json.JSONDecodeError, AttributeError):
        # Model didn't return clean JSON — degrade gracefully rather than crash.
        return {"answer": raw_text.strip(), "used_excerpt_indices": list(range(len(chunks)))}
