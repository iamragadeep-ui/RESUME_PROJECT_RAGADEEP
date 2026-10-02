from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    session_id: str = "demo-session"
    user_id: str = "demo-user"
    user_query: str = ""
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    intent: Optional[Dict[str, Any]] = None
    entities: Dict[str, Any] = Field(default_factory=dict)
    retrieved_data: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list)
    investigation_result: Optional[Dict[str, Any]] = None
    proposed_actions: List[Dict[str, Any]] = Field(default_factory=list)
    tool_results: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0
    validation_result: Optional[Dict[str, Any]] = None
    human_approval: Optional[Dict[str, Any]] = None
    errors: List[str] = Field(default_factory=list)
    final_response: str = ""
    workflow_stage: str = "triage"
    workflow_id: str = "demo-workflow"


class WorkflowDecision(BaseModel):
    next_agent: str
    route: Literal["continue", "needs_more_data", "human_review", "response", "action"]
    reason: str
    requires_human_review: bool = False
