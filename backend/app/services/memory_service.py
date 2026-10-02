from __future__ import annotations

import json
from collections import defaultdict, deque
from typing import Any, Deque, Dict, List


class MemoryService:
    def __init__(self) -> None:
        self.session_store: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.workflow_store: Dict[str, Dict[str, Any]] = {}

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.session_store[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return list(self.session_store.get(session_id, []))

    def save_workflow(self, workflow_id: str, state: Dict[str, Any]) -> None:
        self.workflow_store[workflow_id] = state

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self.workflow_store.get(workflow_id, {})
