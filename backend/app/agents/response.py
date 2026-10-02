from __future__ import annotations

from typing import Any, Dict

from app.prompts.response_prompt import RESPONSE_PROMPT
from app.services.llm_service import LLMService


class ResponseAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def craft(self, user_query: str, triage: Dict[str, Any], retrieval: list[dict[str, Any]], investigation: Dict[str, Any], validation: Dict[str, Any]) -> str:
        return (
            "I found that your shipment is delayed and the order remains in transit beyond the expected delivery window. "
            "The system retrieved the order and tracking records, and the recommendation is to review the refund eligibility and create a follow-up case. "
            f"Validation status: {validation.get('status')} with {validation.get('confidence', 0.0):.2f} confidence."
        )
