from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.graph.workflow import WorkflowEngine
from app.models.schemas import ApprovalRequest, ChatRequest, HealthResponse, WorkflowResponse
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from app.tools.mock_tools import create_ticket, get_customer, get_order, get_ticket_history, get_tracking, request_refund, send_notification

settings = get_settings()
app = FastAPI(title="Delivery Support Resolution Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow_engine = WorkflowEngine()
memory = MemoryService()
llm = LLMService()


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="delivery-support-resolution-agent")


@app.get("/api/metrics")
def metrics() -> dict:
    return {"status": "ok", "workflows": len(workflow_engine._state_store), "sessions": len(memory.session_store)}


@app.post("/api/chat")
def chat(request: ChatRequest):
    workflow = workflow_engine.start(request.session_id, request.user_id, request.message)
    memory.add_message(request.session_id, "user", request.message)
    intent = {
        "intent": "order_delay_support",
        "category": "delivery_issue",
        "priority": "high",
        "entities": {"order_id": "ORD-4419", "customer_id": "CUST1001"},
        "missing_information": [],
        "confidence": 0.91,
        "recommended_route": "retrieve_order_and_policy",
    }
    workflow.intent = intent
    workflow.workflow_stage = "retrieval"
    workflow.retrieved_data = [get_order("ORD-4419"), get_tracking("ORD-4419")]
    response_text = (
        "I reviewed the order and shipment status. The package is delayed and a policy review may support a refund or escalate for carrier follow-up."
    )
    memory.add_message(request.session_id, "assistant", response_text)
    workflow.final_response = response_text
    workflow_engine.update(workflow.workflow_id, final_response=response_text)
    return {"workflow_id": workflow.workflow_id, "response": response_text, "status": "ok"}


@app.post("/api/agent/run")
def agent_run(request: ChatRequest):
    workflow = workflow_engine.start(request.session_id, request.user_id, request.message)
    workflow.workflow_stage = "triage"
    workflow.intent = {
        "intent": "delivery_delay",
        "category": "shipping_issue",
        "priority": "high",
        "confidence": 0.9,
        "missing_information": [],
        "recommended_route": "investigate",
    }
    return {
        "workflow_id": workflow.workflow_id,
        "status": "started",
        "stage": workflow.workflow_stage,
        "message": "Supervisor has routed the request to retrieval and investigation.",
    }


@app.post("/api/documents/upload")
def upload_document():
    return {"status": "accepted", "document_id": f"doc-{uuid4()}"}


@app.post("/api/documents/ingest")
def ingest_documents():
    return {"status": "ingested", "documents": 0}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    return {"session_id": session_id, "history": memory.get_history(session_id)}


@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    state = workflow_engine.get_state(workflow_id)
    return state.model_dump()


@app.post("/api/approval/{workflow_id}")
def approval(workflow_id: str, approval: ApprovalRequest):
    if approval.decision == "approve":
        return {"workflow_id": workflow_id, "status": "approved", "action": "refund_requested"}
    return {"workflow_id": workflow_id, "status": approval.decision, "action": "paused"}
