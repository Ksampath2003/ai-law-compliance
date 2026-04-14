from sqlalchemy import String, Text, ARRAY, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum
from app.db.database import Base


class LawStatus(str, enum.Enum):
    active = "active"
    pending = "pending"
    failed = "failed"
    repealed = "repealed"


class RiskLevel(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Law(Base):
    __tablename__ = "laws"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    full_text: Mapped[str] = mapped_column(Text, nullable=True)
    plain_english_summary: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[LawStatus] = mapped_column(SAEnum(LawStatus), default=LawStatus.pending, index=True)
    effective_date: Mapped[str] = mapped_column(String(32), nullable=True)
    ai_category: Mapped[str] = mapped_column(String(128), nullable=True)  # e.g. "LLM", "Computer Vision", "Automated Decision"
    industries_affected: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    risk_level: Mapped[RiskLevel] = mapped_column(SAEnum(RiskLevel), default=RiskLevel.medium)
    compliance_steps: Mapped[list] = mapped_column(ARRAY(Text), nullable=True)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_ai_relevant: Mapped[bool] = mapped_column(default=True)
    vector_indexed: Mapped[bool] = mapped_column(default=False)
