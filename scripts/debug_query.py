"""Run a transparent, local diagnostic trace without changing application behavior."""
from __future__ import annotations

import argparse
from agents.response import generate_response
from agents.retrieval_agent import retrieve_knowledge
from agents.understanding import understand_context
from agents.validation import validate_cultural_knowledge
from retrieval.vector_store import CulturalVectorStore

DEFAULT_QUERIES = [
    "What should I do at a wedding?",
    "What is the most common dish in Central Saudi Arabia?",
    "As an international student in Riyadh, what should I know before attending a social gathering?",
    "What is the etiquette for visiting Mars?",
]

def trace(query: str) -> None:
    store = CulturalVectorStore()
    state: dict = {"query": query, "conversation_context": "", "attempts": 0}
    state.update(understand_context(state))
    print(f"\n=== QUERY: {query}")
    print("context:", {key: state.get(key) for key in ("region", "user_role", "occasion", "category", "retrieval_query")})
    print("collection count:", store.collection.count())
    state.update(retrieve_knowledge(store)(state))
    raw = state["raw_semantic_results"]
    print(f"raw semantic results: {len(raw)}")
    for item in raw:
        print(f"  region={item['region']}; category={item['category']}; distance={item['distance']:.4f}; relevance={item['relevance']:.4f}; question={item['question']}")
    print("after metadata filter:", len(state["retrieved"]))
    state.update(validate_cultural_knowledge(state))
    print("after evidence validation:", len(state["validated"]))
    print("validation reason:", state["validation_reason"])
    state.update(generate_response(state))
    print("final status:", state["status"], "| final validated count:", len(state.get("validated", [])))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", help="One query to trace; omit to trace the four diagnostic queries.")
    args = parser.parse_args()
    for query in [" ".join(args.query)] if args.query else DEFAULT_QUERIES:
        trace(query)
