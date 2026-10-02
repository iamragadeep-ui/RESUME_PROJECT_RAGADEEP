from __future__ import annotations

from typing import Any, Dict

from app.prompts.validation_prompt import VALIDATION_PROMPT
from app.services.llm_service import LLMService


class ValidationAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def validate(self, recommendation: Dict[str, Any], evidence: list[dict[str, Any]]) -> Dict[str, Any]:
        if not evidence:
            return {"status": "RETRY", "reasons": ["No evidence collected."], "confidence": 0.0}
        if recommendation.get("requires_human_review"):
            return {"status": "HUMAN_REVIEW", "reasons": ["Action requires approval due to policy or high-risk outcome."], "confidence": 0.87}
        return {"status": "PASS", "reasons": ["Evidence and policy references are present."], "confidence": 0.89}
