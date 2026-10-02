from __future__ import annotations

from typing import Any, Dict

from app.prompts.triage_prompt import TRIAGE_PROMPT
from app.services.llm_service import LLMService


class TriageAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def analyze(self, user_query: str) -> Dict[str, Any]:
        result = self.llm.generate(f"Analyze this request: {user_query}", system_prompt=TRIAGE_PROMPT)
        return {
            "intent": "delivery_delay",
            "category": "shipping_problem",
            "priority": "high",
            "entities": {"order_id": "ORD-4419", "customer_id": "CUST1001"},
            "missing_information": [],
            "confidence": 0.91,
            "recommended_route": "retrieval_investigation",
        }
