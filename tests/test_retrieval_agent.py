from agents.retrieval_agent import retrieve_knowledge
from retrieval.models import KnowledgeRecord, RetrievedKnowledge

class FakeStore:
    def __init__(self):
        self.calls = []
    def search(self, query, region, limit):
        self.calls.append((query, region, limit))
        return [RetrievedKnowledge(KnowledgeRecord("1", "What food?", "A dataset answer", "", "East", "Common", "Food", "Open-ended"), 0.9)]

def test_retrieval_passes_region_filter_to_store():
    store = FakeStore()
    result = retrieve_knowledge(store)({"retrieval_query": "food", "region": "East"})
    assert store.calls == [("food", "East", 5)]
    assert result["retrieved"][0]["region"] == "East"
