from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class LawStatus(str, Enum):
    active = "active"
    pending = "pending"
    failed = "failed"
    repealed = "repealed"


class RiskLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class LawBase(BaseModel):
    title: str
    state: str = Field(..., min_length=2, max_length=2, description="2-letter state code")
    summary: str
    full_text: Optional[str] = None
    status: LawStatus = LawStatus.pending
    effective_date: Optional[str] = None
    ai_category: Optional[str] = None
    industries_affected: Optional[List[str]] = []
    risk_level: RiskLevel = RiskLevel.medium
    compliance_steps: Optional[List[str]] = []
    source_url: Optional[str] = None


class LawCreate(LawBase):
    id: Optional[str] = None


class LawRead(LawBase):
    id: str
    plain_english_summary: Optional[str] = None
    last_updated: datetime
    is_ai_relevant: bool
    vector_indexed: bool

    class Config:
        from_attributes = True


class LawListItem(BaseModel):
    id: str
    title: str
    state: str
    status: LawStatus
    risk_level: RiskLevel
    ai_category: Optional[str]
    effective_date: Optional[str]
    plain_english_summary: Optional[str]

    class Config:
        from_attributes = True


# ── Compliance ────────────────────────────────────────────────────────────────

class ComplianceRequest(BaseModel):
    industry: str = Field(..., description="e.g. healthcare, fintech, retail")
    state: str = Field(..., min_length=2, max_length=2)
    ai_usage_types: List[str] = Field(
        ..., description="e.g. ['LLM', 'computer_vision', 'automated_decision']"
    )
    company_description: Optional[str] = None


class LawApplicability(BaseModel):
    law_id: str
    law_title: str
    applicable: bool
    reason: str
    risk_level: RiskLevel
    compliance_steps: List[str]
    status: LawStatus


class ComplianceResponse(BaseModel):
    state: str
    industry: str
    ai_usage_types: List[str]
    applicable_laws: List[LawApplicability]
    total_laws_checked: int
    high_risk_count: int
    summary: str


# ── Search ────────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    state: Optional[str] = None
    status: Optional[LawStatus] = None
    risk_level: Optional[RiskLevel] = None
    top_k: int = Field(default=10, le=50)


class SearchResult(BaseModel):
    law: LawListItem
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int


# ── Ingest ────────────────────────────────────────────────────────────────────

class IngestRequest(BaseModel):
    laws: List[LawCreate]
    run_ai_filter: bool = True
    generate_summaries: bool = True


class IngestResponse(BaseModel):
    processed: int
    accepted: int
    rejected: int
    errors: List[str]
