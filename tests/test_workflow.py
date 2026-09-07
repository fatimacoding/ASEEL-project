from agents.understanding import understand_context
from agents.response import generate_response
from agents.validation import validate_cultural_knowledge
from workflow.graph import route_after_validation

def test_understanding_extracts_region_and_role():
    result = understand_context({"query": "As a tourist visiting the East, what should I eat?"})
    assert result["region"] == "East"
    assert result["user_role"] == "Tourist"

def test_validation_rejects_irrelevant_knowledge(monkeypatch):
    monkeypatch.setattr("agents.validation.MIN_RELEVANCE", 0.7)
    state = {"region": "East", "retrieved": [{"region": "East", "relevance": 0.2}]}
    result = validate_cultural_knowledge(state)
    assert result["validated"] == []
    assert route_after_validation({**state, **result, "attempts": 1}) == "respond"

def test_validation_rejects_wrong_region(monkeypatch):
    monkeypatch.setattr("agents.validation.MIN_RELEVANCE", 0.1)
    result = validate_cultural_knowledge({"region": "East", "retrieved": [{"region": "West", "relevance": 0.9}]})
    assert result["validated"] == []

def test_fallback_when_no_knowledge_is_available():
    result = generate_response({"query": "What is the etiquette on Mars?", "validated": []})
    assert result["status"] == "fallback"
    assert "could not find" in result["answer"]

def test_grounded_response_uses_validated_facts(monkeypatch):
    monkeypatch.setattr("agents.response.OPENAI_API_KEY", None)
    result = generate_response({"query": "Question", "region": "East", "validated": [{"region": "East", "answer": "Dataset answer", "question": "Dataset question", "category": "Food"}]})
    assert result["status"] == "grounded"
    assert "Dataset answer" in result["answer"]
