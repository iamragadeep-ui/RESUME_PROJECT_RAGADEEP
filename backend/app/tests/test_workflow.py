from app.agents.triage import TriageAgent
from app.graph.workflow import WorkflowEngine
from app.models.schemas import ChatRequest


def test_triage_agent_returns_structured_fields() -> None:
    agent = TriageAgent()
    result = agent.analyze("My order is delayed and I need an update for ORD-4419.")
    assert result["intent"]
    assert result["category"]
    assert result["priority"] in {"low", "medium", "high", "urgent"}
    assert "entities" in result


def test_workflow_engine_tracks_workflow() -> None:
    engine = WorkflowEngine()
    state = engine.start("session-1", "user-1", "Delayed delivery")
    assert state.workflow_id
    assert state.user_query == "Delayed delivery"
    saved = engine.get_state(state.workflow_id)
    assert saved.session_id == "session-1"
