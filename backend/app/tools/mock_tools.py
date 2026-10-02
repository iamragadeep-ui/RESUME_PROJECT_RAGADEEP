from __future__ import annotations

from typing import Any, Dict, List


CUSTOMER_DB = {
    "CUST1001": {"name": "Ava Patel", "status": "gold", "orders": ["ORD-4401", "ORD-4419"]},
    "CUST1002": {"name": "Leo Martin", "status": "silver", "orders": ["ORD-5520"]},
    "CUST1003": {"name": "Sofia Nguyen", "status": "gold", "orders": ["ORD-9982"]},
}

ORDER_DB = {
    "ORD-4401": {
        "customer_id": "CUST1001",
        "status": "IN_TRANSIT",
        "carrier": "NorthStar",
        "tracking_number": "NS-889123",
        "expected_delivery": "2026-10-04",
        "amount": 129.99,
        "address": "15 Lake Street, Austin, TX",
    },
    "ORD-4419": {
        "customer_id": "CUST1001",
        "status": "DELAYED",
        "carrier": "NorthStar",
        "tracking_number": "NS-889456",
        "expected_delivery": "2026-10-05",
        "amount": 85.0,
        "address": "15 Lake Street, Austin, TX",
    },
    "ORD-5520": {
        "customer_id": "CUST1002",
        "status": "DELIVERED",
        "carrier": "RapidFreight",
        "tracking_number": "RF-912233",
        "expected_delivery": "2026-09-30",
        "amount": 64.5,
        "address": "88 Pine Avenue, Denver, CO",
    },
    "ORD-9982": {
        "customer_id": "CUST1003",
        "status": "PROCESSING",
        "carrier": "AirRoute",
        "tracking_number": "AR-331055",
        "expected_delivery": "2026-10-08",
        "amount": 220.0,
        "address": "21 Harbor Lane, Seattle, WA",
    },
}

CASE_DB = {
    "TKT-2041": {"order_id": "ORD-4419", "summary": "Carrier delay", "priority": "high"},
    "TKT-2100": {"order_id": "ORD-5520", "summary": "Late delivery refund request", "priority": "medium"},
}


class ToolError(Exception):
    pass


def get_customer(customer_id: str) -> Dict[str, Any]:
    customer = CUSTOMER_DB.get(customer_id)
    if not customer:
        raise ToolError(f"Customer not found: {customer_id}")
    return customer


def get_order(order_id: str) -> Dict[str, Any]:
    order = ORDER_DB.get(order_id)
    if not order:
        raise ToolError(f"Order not found: {order_id}")
    return order


def get_tracking(order_id: str) -> Dict[str, Any]:
    order = get_order(order_id)
    return {
        "status": order["status"],
        "carrier": order["carrier"],
        "tracking_number": order["tracking_number"],
        "expected_delivery": order["expected_delivery"],
    }


def get_ticket_history(customer_id: str) -> List[Dict[str, Any]]:
    results = []
    for case_id, case in CASE_DB.items():
        if case["order_id"] in ORDER_DB and ORDER_DB[case["order_id"]]["customer_id"] == customer_id:
            results.append({"ticket_id": case_id, **case})
    return results


def create_ticket(order_id: str, summary: str, priority: str = "medium") -> Dict[str, Any]:
    ticket_id = f"TKT-{len(CASE_DB) + 1000}"
    CASE_DB[ticket_id] = {"order_id": order_id, "summary": summary, "priority": priority}
    return {"ticket_id": ticket_id, "status": "created", "summary": summary, "priority": priority}


def request_refund(order_id: str, amount: float, reason: str) -> Dict[str, Any]:
    order = get_order(order_id)
    return {
        "order_id": order_id,
        "amount": amount,
        "reason": reason,
        "status": "approved_for_review",
        "customer_id": order["customer_id"],
    }


def send_notification(customer_id: str, message: str) -> Dict[str, Any]:
    return {"customer_id": customer_id, "status": "queued", "message": message}
