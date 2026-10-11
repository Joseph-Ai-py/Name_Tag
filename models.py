from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class BrandData(BaseModel):
    business_type: str = ""
    vibes: list[str] = Field(default_factory=list)
    target: str = ""
    keywords: str = ""
    initial_idea: str = ""


class DecisionTrace(BaseModel):
    trace_id: str
    stage: str
    decision_type: str
    user_input: str
    ai_interpretation: str
    brand_decision: str
    rationale: str
    source_question_ids: list[int] = Field(default_factory=list)
    status: str = "ai_derived"


class BrandDNA(BaseModel):
    foundation: dict[str, Any] = Field(default_factory=dict)
    why: dict[str, Any] = Field(default_factory=dict)
    who: dict[str, Any] = Field(default_factory=dict)
    promise: dict[str, Any] = Field(default_factory=dict)
    position: dict[str, Any] = Field(default_factory=dict)
    voice: dict[str, Any] = Field(default_factory=dict)
    visual: dict[str, Any] = Field(default_factory=dict)
    behavior: dict[str, Any] = Field(default_factory=dict)
    business: dict[str, Any] = Field(default_factory=dict)


class IntegrityIssue(BaseModel):
    severity: str
    category: str
    source_stage: str
    field: str
    problematic_text: str
    reason: str
    suggested_fix: str


class BrandIntegrityReport(BaseModel):
    status: str
    issues: list[IntegrityIssue] = Field(default_factory=list)


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    stage: str | None = None
    topic: str | None = None


class ConversationQuestion(BaseModel):
    question_id: str
    topic: str
    question_text: str
    options: list[str] = Field(min_length=4, max_length=4)


class ProposedUpdate(BaseModel):
    path: str
    value: Any
    interpretation: str
    status: Literal["ai_suggested", "ai_derived"] = "ai_suggested"


class ConversationTurn(BaseModel):
    assistant_message: str
    question: ConversationQuestion | None = None
    extracted_facts: list[str] = Field(default_factory=list)
    proposed_updates: list[ProposedUpdate] = Field(default_factory=list)
    next_focus: str = "foundation"
    snapshot_ready: bool = False


class ConversationState(BaseModel):
    messages: list[ConversationMessage] = Field(default_factory=list)
    conversation_summary: str = ""
    current_focus: str | None = None
    covered_topics: list[str] = Field(default_factory=list)
    missing_topics: list[str] = Field(default_factory=list)
    initial_idea: str | None = None
    interview_progress: dict[str, Any] = Field(default_factory=dict)
    raw_results: dict[str, Any] = Field(default_factory=dict)
    structured_context: dict[str, Any] = Field(default_factory=dict)
    decision_traces: list[dict[str, Any]] = Field(default_factory=list)


class BrandDocument(BaseModel):
    identity: dict[str, Any] = Field(default_factory=dict)
    strategy: dict[str, Any] = Field(default_factory=dict)
    customer: dict[str, Any] = Field(default_factory=dict)
    business: dict[str, Any] = Field(default_factory=dict)
    visual: dict[str, Any] = Field(default_factory=dict)
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    integrity: dict[str, Any] = Field(default_factory=dict)
