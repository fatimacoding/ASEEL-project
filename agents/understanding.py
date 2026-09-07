from __future__ import annotations
import re
from agents.state import AseelState

REGIONS = ("West", "East", "North", "South", "Central", "General")
ROLES = ("tourist", "visitor", "resident", "student", "expat")
OCCASIONS = ("majlis", "wedding", "restaurant", "meal", "dinner", "meeting", "campus", "celebration", "visit")

def _match(options: tuple[str, ...], text: str) -> str | None:
    lowered = text.lower()
    return next((item.title() for item in options if re.search(rf"\b{re.escape(item)}\b", lowered)), None)

def understand_context(state: AseelState) -> dict:
    text = f"{state.get('conversation_context', '')} {state['query']}"
    region = _match(REGIONS, text)
    return {"region": region, "user_role": _match(ROLES, text), "occasion": _match(OCCASIONS, text), "intent": "cultural etiquette guidance", "retrieval_query": state["query"], "attempts": state.get("attempts", 0)}
