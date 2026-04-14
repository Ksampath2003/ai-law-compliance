from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.database import get_db
from app.models.law import Law
from app.schemas.law import ComplianceRequest, ComplianceResponse, RiskLevel
from app.services.compliance import analyze_law_applicability, generate_compliance_summary

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])


@router.post("/analyze", response_model=ComplianceResponse)
async def analyze_compliance(
    request: ComplianceRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Analyze which AI laws apply to your company.
    Provide your industry, state, and the types of AI you use.
    """
    # Fetch relevant laws for the state
    result = await db.execute(
        select(Law).where(
            and_(Law.state == request.state.upper(), Law.is_ai_relevant == True)
        )
    )
    laws = result.scalars().all()

    if not laws:
        return ComplianceResponse(
            state=request.state,
            industry=request.industry,
            ai_usage_types=request.ai_usage_types,
            applicable_laws=[],
            total_laws_checked=0,
            high_risk_count=0,
            summary=f"No AI laws tracked yet for {request.state}. Check back as legislation develops.",
        )

    # Analyze each law
    from app.schemas.law import LawRead
    applicability_results = []
    for law in laws:
        law_schema = LawRead.model_validate(law)
        applicability = analyze_law_applicability(law_schema, request)
        if applicability.applicable:
            applicability_results.append(applicability)

    high_risk = sum(1 for l in applicability_results if l.risk_level == RiskLevel.high)
    summary = generate_compliance_summary(
        state=request.state,
        industry=request.industry,
        applicable_laws=applicability_results,
    )

    return ComplianceResponse(
        state=request.state,
        industry=request.industry,
        ai_usage_types=request.ai_usage_types,
        applicable_laws=applicability_results,
        total_laws_checked=len(laws),
        high_risk_count=high_risk,
        summary=summary,
    )
