from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    session_id: str = "demo-session"
    user_id: str = "demo-user"
    message: str
    conversation_history: List[ChatMessage] = Field(default_factory=list)


class TriageResult(BaseModel):
    intent: str
    category: str
    priority: Literal["low", "medium", "high", "urgent"]
    entities: Dict[str, Any] = Field(default_factory=dict)
    missing_information: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    recommended_route: str


class RetrievalResult(BaseModel):
    source: str
    title: str
    excerpt: str
    section: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InvestigationResult(BaseModel):
    issue_type: str
    evidence: List[str] = Field(default_factory=list)
    policy_reference: List[str] = Field(default_factory=list)
    recommended_action: str
    confidence: float = 0.0
    requires_human_review: bool = False


class ValidationResult(BaseModel):
    status: Literal["PASS", "RETRY", "HUMAN_REVIEW", "BLOCK"]
    reasons: List[str] = Field(default_factory=list)
    confidence: float = 0.0


class ApprovalRequest(BaseModel):
    workflow_id: str
    decision: Literal["approve", "reject", "modify"]
    notes: Optional[str] = None


class WorkflowResponse(BaseModel):
    workflow_id: str
    session_id: str
    status: str
    final_response: str
    citations: List[str] = Field(default_factory=list)
    validation: Optional[ValidationResult] = None
    requires_human_approval: bool = False


class HealthResponse(BaseModel):
    status: str
    service: str
