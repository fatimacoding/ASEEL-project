from __future__ import annotations
from agents.state import AseelState
from retrieval.vector_store import CulturalVectorStore
from tools.cultural_search import search_cultural_knowledge

def retrieve_knowledge(store: CulturalVectorStore):
    def node(state: AseelState) -> dict:
        results = search_cultural_knowledge(store, state["retrieval_query"], state.get("region"), limit=5)
        return {"retrieved": [{"question": x.record.question, "answer": x.record.answer, "region": x.record.region, "domain": x.record.domain, "category": x.record.category, "relevance": x.relevance} for x in results]}
    return node
