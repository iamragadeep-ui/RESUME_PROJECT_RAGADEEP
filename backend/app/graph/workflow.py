from __future__ import annotations

import uuid
from typing import Any, Dict, List

from app.graph.state import AgentState


class WorkflowEngine:
    def __init__(self) -> None:
        self._state_store: Dict[str, AgentState] = {}

    def start(self, session_id: str, user_id: str, message: str) -> AgentState:
        workflow_id = str(uuid.uuid4())
        state = AgentState(
            session_id=session_id,
            user_id=user_id,
            user_query=message,
            workflow_id=workflow_id,
        )
        self._state_store[workflow_id] = state
        return state

    def get_state(self, workflow_id: str) -> AgentState:
        return self._state_store.get(workflow_id, AgentState())

    def update(self, workflow_id: str, **kwargs: Any) -> AgentState:
        state = self._state_store.get(workflow_id, AgentState())
        for key, value in kwargs.items():
            if hasattr(state, key):
                setattr(state, key, value)
        self._state_store[workflow_id] = state
        return state

    def list_runs(self) -> List[Dict[str, Any]]:
        return [{"workflow_id": key, "state": value.model_dump()} for key, value in self._state_store.items()]
