from __future__ import annotations

from typing import Any, Dict, List

from app.prompts.retrieval_prompt import RETRIEVAL_PROMPT
from app.services.llm_service import LLMService
from app.tools.mock_tools import get_order, get_tracking, get_ticket_history


class RetrievalAgent:
    def __init__(self) -> None:
        self.llm = LLMService()

    def fetch(self, triage: Dict[str, Any]) -> List[Dict[str, Any]]:
        order_id = triage.get("entities", {}).get("order_id", "ORD-4419")
        customer_id = triage.get("entities", {}).get("customer_id", "CUST1001")
        order = get_order(order_id)
        tracking = get_tracking(order_id)
        history = get_ticket_history(customer_id)
        return [
            {"source": "order_api", "title": "Order Record", "excerpt": str(order), "section": "order", "score": 0.99},
            {"source": "tracking_api", "title": "Shipment Status", "excerpt": str(tracking), "section": "tracking", "score": 0.97},
            {"source": "ticket_history", "title": "Customer Case History", "excerpt": str(history), "section": "history", "score": 0.92},
        ]
