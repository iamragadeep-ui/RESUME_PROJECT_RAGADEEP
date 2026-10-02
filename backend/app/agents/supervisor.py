from __future__ import annotations

from typing import Any, Dict

from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT
from app.services.llm_service import LLMService


class SupervisorAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def decide(self, user_query: str, triage: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"User query: {user_query}\nTriage: {triage}"
        result = self.llm.generate(prompt, system_prompt=SUPERVISOR_PROMPT)
        if "human_review" in result.lower():
            return {"next_agent": "human_review", "route": "human_review", "reason": "High-risk action or low-confidence recommendation", "requires_human_review": True}
        if triage.get("priority") in {"high", "urgent"}:
            return {"next_agent": "investigation", "route": "continue", "reason": "Escalate to investigation and retrieval", "requires_human_review": False}
        return {"next_agent": "retrieval", "route": "continue", "reason": "Collect supporting evidence", "requires_human_review": False}
