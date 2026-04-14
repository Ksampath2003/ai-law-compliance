"""
Core compliance analysis: given a company's profile, determine which laws
apply and generate actionable compliance checklists.
"""
from typing import List
from app.schemas.law import (
    ComplianceRequest, ComplianceResponse, LawApplicability, LawRead, RiskLevel
)
from app.services.llm import call_claude_json


def analyze_law_applicability(
    law: LawRead,
    request: ComplianceRequest,
) -> LawApplicability:
    """Ask Claude whether a specific law applies to the company."""

    result = call_claude_json(
        prompt=f"""Does this AI law apply to the company described below?

=== LAW ===
Title: {law.title}
State: {law.state}
Summary: {law.summary}
AI Category: {law.ai_category}
Industries Affected: {", ".join(law.industries_affected or ["all"])}
Risk Level: {law.risk_level}
Status: {law.status}

=== COMPANY ===
Industry: {request.industry}
State: {request.state}
AI Usage Types: {", ".join(request.ai_usage_types)}
Description: {request.company_description or "Not provided"}

Respond with JSON:
{{
  "applicable": true/false,
  "reason": "2-3 sentence explanation",
  "compliance_steps": ["step 1", "step 2", "step 3"]
}}""",
        system="You are a legal compliance expert specializing in AI regulation. Be direct and practical.",
        max_tokens=512,
    )

    return LawApplicability(
        law_id=law.id,
        law_title=law.title,
        applicable=result.get("applicable", False),
        reason=result.get("reason", ""),
        risk_level=law.risk_level,
        compliance_steps=result.get("compliance_steps", law.compliance_steps or []),
        status=law.status,
    )


def generate_compliance_summary(
    state: str,
    industry: str,
    applicable_laws: List[LawApplicability],
) -> str:
    if not applicable_laws:
        return f"No applicable AI laws found for {industry} companies in {state}. Monitor for upcoming legislation."

    high = [l for l in applicable_laws if l.risk_level == RiskLevel.high]
    medium = [l for l in applicable_laws if l.risk_level == RiskLevel.medium]

    result = call_claude_json(
        prompt=f"""Write a 2-3 sentence executive summary for a {industry} company in {state}.
They must comply with {len(applicable_laws)} AI laws ({len(high)} high risk, {len(medium)} medium risk).
High-risk laws: {[l.law_title for l in high]}

Respond: {{"summary": "..."}}""",
        system="You are a concise compliance advisor.",
        max_tokens=256,
    )
    return result.get("summary", "Review applicable laws and implement compliance steps promptly.")


def generate_plain_english_summary(title: str, full_text: str) -> str:
    """Generate a plain-English summary of a law for non-lawyers."""
    result = call_claude_json(
        prompt=f"""Summarize this AI law in plain English for a non-lawyer business owner.
Keep it under 100 words. Focus on: what it requires, who it affects, and the key deadline.

Law Title: {title}
Text: {full_text[:3000]}

Respond: {{"summary": "..."}}""",
        system="You are an expert at making legal language accessible.",
        max_tokens=256,
    )
    return result.get("summary", "")
