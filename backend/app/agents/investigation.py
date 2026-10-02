from __future__ import annotations

from typing import Any, Dict

from app.prompts.investigation_prompt import INVESTIGATION_PROMPT
from app.services.llm_service import LLMService


class InvestigationAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def assess(self, retrieved_data: list[dict[str, Any]]) -> Dict[str, Any]:
        return {
            "issue_type": "Carrier delay",
            "evidence": ["Order status is DELAYED", "Carrier tracking confirms delay beyond expected delivery window"],
            "policy_reference": ["shipping_policy:v1#late-delivery", "customer_service_policy:v2#delay-credit"],
            "recommended_action": "Offer delayed-shipment follow-up and refund review if policy criteria are met",
            "confidence": 0.88,
            "requires_human_review": True,
        }
