from __future__ import annotations
from agents.state import AseelState
from config.settings import MIN_RELEVANCE

def validate_cultural_knowledge(state: AseelState) -> dict:
    requested = state.get("region")
    valid = [item for item in state.get("retrieved", []) if item["relevance"] >= MIN_RELEVANCE and (not requested or item["region"] == requested)]
    reason = "Grounded in retrieved regional records." if valid else "No sufficiently relevant, region-compatible knowledge record was found."
    return {"validated": valid, "status": "grounded" if valid else "pending", "validation_reason": reason}

def refine_query(state: AseelState) -> dict:
    # A deliberately conservative retry: expands terminology but never adds cultural facts.
    query = state["query"]
    if state.get("occasion"):
        query = f"{query} {state['occasion']} etiquette customs"
    return {"retrieval_query": query, "attempts": state.get("attempts", 0) + 1}
