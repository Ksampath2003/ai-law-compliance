#!/usr/bin/env python3
"""
Seed the database with a curated set of real U.S. AI laws for MVP demo.
Run: python scripts/seed_laws.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.law import Law, LawStatus, RiskLevel
from app.db.database import Base
from app.db.vector_store import vector_store
from app.services.embeddings import embed_law

SYNC_URL = settings.DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(SYNC_URL)

SEED_LAWS = [
    {
        "id": "ca-ab-2013-2023",
        "title": "California AB 2013 — AI Training Data Transparency",
        "state": "CA",
        "summary": "Requires developers of generative AI systems to publicly disclose the datasets used to train their models, including data sources, collection methods, and whether copyrighted or personal data was used.",
        "full_text": "An act relating to artificial intelligence training data transparency. Generative AI providers must post on their website the data used to train generative AI systems offered to Californians. Disclosure must include: types of data, sources of data, whether personal information was included, and whether copyrighted material was licensed.",
        "plain_english_summary": "If you build or sell generative AI in California, you must publicly list what data you trained your model on — including whether you used personal data or copyrighted content.",
        "status": "active",
        "effective_date": "2026-01-01",
        "ai_category": "Generative AI / LLM",
        "industries_affected": ["technology", "healthcare", "finance", "retail", "media"],
        "risk_level": "high",
        "compliance_steps": [
            "Audit and document all training datasets used in your AI models",
            "Create a public-facing transparency page on your website",
            "Disclose data sources, types (personal/copyrighted), and licensing status",
            "Establish a process to update disclosures when models are retrained",
            "Consult legal counsel to ensure CCPA alignment",
        ],
        "source_url": "https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013",
    },
    {
        "id": "ca-sb-1047-2024",
        "title": "California SB 1047 — Safe and Secure Innovation for Frontier AI Models Act",
        "state": "CA",
        "summary": "Imposes safety obligations on developers of large AI models that cost over $100 million to train, requiring safety testing, incident reporting, and a kill switch capability.",
        "full_text": "Requires developers of covered AI models (training cost exceeding $100M) to implement and maintain a written safety and security protocol. Developers must perform pre-deployment safety testing, maintain capability to shut down models, and report safety incidents to the California Government Operations Agency.",
        "plain_english_summary": "Companies that spend $100M+ training AI models must document safety practices, test for dangerous capabilities before launch, and be able to shut down their models if something goes wrong.",
        "status": "pending",
        "effective_date": "2026-01-01",
        "ai_category": "Foundation Models / LLM",
        "industries_affected": ["technology", "research", "defense"],
        "risk_level": "high",
        "compliance_steps": [
            "Determine if your model's training costs exceed $100M threshold",
            "Develop a written safety and security protocol",
            "Implement pre-deployment safety evaluation procedures",
            "Build capability to disable model (kill switch) within your infrastructure",
            "Establish incident reporting pipeline to California Gov Ops Agency",
            "Retain audit logs of safety evaluations",
        ],
        "source_url": "https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB1047",
    },
    {
        "id": "il-sb-2533-2024",
        "title": "Illinois SB 2533 — Artificial Intelligence Video Interview Act",
        "state": "IL",
        "summary": "Requires employers using AI to analyze video interviews to notify candidates, obtain consent, explain how AI is used, and limit sharing of video data.",
        "full_text": "Employers that use artificial intelligence analysis of video interviews must: notify applicants before the interview that AI may be used, explain the general types of characteristics AI will use, obtain consent, only share videos with those whose expertise is necessary to evaluate the applicant, and delete videos within 30 days of request.",
        "plain_english_summary": "Illinois employers using AI to screen video interviews must tell candidates upfront, get their consent, and delete recordings within 30 days of being asked.",
        "status": "active",
        "effective_date": "2020-01-01",
        "ai_category": "Computer Vision / Automated Decision",
        "industries_affected": ["healthcare", "finance", "retail", "technology", "manufacturing", "staffing"],
        "risk_level": "high",
        "compliance_steps": [
            "Audit all video interview platforms for AI analysis features",
            "Add AI disclosure notice to all job application workflows",
            "Implement consent collection before video interviews",
            "Document what AI characteristics/traits are being evaluated",
            "Restrict video sharing to essential personnel only",
            "Implement 30-day video deletion process upon candidate request",
        ],
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=4015",
    },
    {
        "id": "tx-sb-2232-2023",
        "title": "Texas SB 2232 — Artificial Intelligence in State Agency Decision-Making",
        "state": "TX",
        "summary": "Requires Texas state agencies that use AI systems in consequential decisions affecting Texans to conduct impact assessments, maintain human oversight, and provide appeal mechanisms.",
        "full_text": "State agencies must conduct annual impact assessments for AI systems used in consequential decisions. Assessments must evaluate accuracy, bias, and disparate impact across demographic groups. Agencies must maintain human review capability for AI decisions and provide affected individuals a right to appeal automated decisions.",
        "plain_english_summary": "Texas agencies using AI in decisions that affect people's lives must annually audit their systems for bias and must allow people to appeal any automated decision.",
        "status": "active",
        "effective_date": "2024-09-01",
        "ai_category": "Automated Decision Systems",
        "industries_affected": ["government", "healthcare", "social_services"],
        "risk_level": "medium",
        "compliance_steps": [
            "Inventory all AI systems used in consequential decisions",
            "Conduct annual AI impact assessments including bias analysis",
            "Document disparate impact findings and remediation steps",
            "Implement human review capability for all automated decisions",
            "Create and publicize an appeal process for AI-driven decisions",
        ],
        "source_url": "https://capitol.texas.gov/BillLookup/History.aspx?LegSess=88R&Bill=SB2232",
    },
    {
        "id": "co-sb-205-2024",
        "title": "Colorado SB 205 — Colorado AI Act (Artificial Intelligence)",
        "state": "CO",
        "summary": "Requires developers and deployers of high-risk AI systems to use reasonable care to protect consumers from algorithmic discrimination, conduct impact assessments, and provide transparency notices.",
        "full_text": "Developers of high-risk AI systems must provide deployers with documentation about known limitations and bias. Deployers must conduct impact assessments, implement risk management policies, provide transparency disclosures to consumers, and offer a process for consumers to appeal consequential AI decisions affecting education, employment, credit, housing, or healthcare.",
        "plain_english_summary": "Colorado companies deploying AI that makes high-stakes decisions about people must assess bias risks, tell users when AI is involved, and let them challenge unfavorable outcomes.",
        "status": "active",
        "effective_date": "2026-02-01",
        "ai_category": "High-Risk AI / Automated Decision",
        "industries_affected": ["finance", "healthcare", "education", "housing", "employment", "insurance"],
        "risk_level": "high",
        "compliance_steps": [
            "Classify your AI systems against Colorado's high-risk criteria",
            "Request and review developer documentation for all third-party AI tools",
            "Conduct algorithmic impact assessments for high-risk deployments",
            "Implement a risk management policy and assign accountability",
            "Add consumer transparency notices to AI-driven touchpoints",
            "Build an appeal/contest mechanism for AI-driven consequential decisions",
            "Prepare annual impact assessment reports",
        ],
        "source_url": "https://leg.colorado.gov/bills/sb24-205",
    },
    {
        "id": "ny-a07859-2023",
        "title": "New York A07859 — Automated Employment Decision Tools",
        "state": "NY",
        "summary": "New York City requires employers using automated employment decision tools to conduct annual bias audits, publish audit results, and notify candidates when such tools are used in hiring decisions.",
        "full_text": "Employers in New York City that use an automated employment decision tool (AEDT) must conduct an independent bias audit of the tool at least annually. Employers must publish a summary of audit results on their website. Before using an AEDT to assess a candidate or employee, the employer must notify the candidate at least 10 business days before.",
        "plain_english_summary": "NYC employers using AI hiring tools must get annual third-party bias audits, post the results publicly, and give candidates 10 days notice before using AI to screen them.",
        "status": "active",
        "effective_date": "2023-07-05",
        "ai_category": "Automated Decision / HR AI",
        "industries_affected": ["technology", "finance", "healthcare", "retail", "staffing", "all"],
        "risk_level": "high",
        "compliance_steps": [
            "Identify all automated employment decision tools used in NYC hiring",
            "Commission an independent bias audit from a qualified third party",
            "Publish bias audit summary on your public-facing careers page",
            "Implement 10-business-day advance notice to candidates",
            "Create an opt-out process for candidates who prefer human review",
            "Schedule annual re-audits and update published results",
        ],
        "source_url": "https://legistar.council.nyc.gov/LegislationDetail.aspx?ID=4344524",
    },
    {
        "id": "wa-sb-5116-2024",
        "title": "Washington SB 5116 — Automated Decision Systems in Government",
        "state": "WA",
        "summary": "Directs Washington state agencies to inventory automated decision systems, conduct algorithmic impact assessments for high-risk systems, and make assessment summaries publicly available.",
        "full_text": "State agencies must inventory all automated decision systems in use. For high-impact systems, agencies must conduct algorithmic impact assessments analyzing accuracy, bias, privacy, and potential for harm. Summaries of assessments for high-impact systems must be made publicly available. Agencies must provide human review options for consequential decisions.",
        "plain_english_summary": "Washington agencies must catalog all their AI decision tools and publicly disclose bias impact assessments for high-stakes systems.",
        "status": "active",
        "effective_date": "2024-07-01",
        "ai_category": "Automated Decision Systems",
        "industries_affected": ["government", "public_services"],
        "risk_level": "medium",
        "compliance_steps": [
            "Complete agency-wide inventory of automated decision systems",
            "Classify systems by impact level per agency guidelines",
            "Conduct algorithmic impact assessments for high-impact systems",
            "Publish assessment summaries on agency website",
            "Implement human review pathways for high-impact decisions",
        ],
        "source_url": "https://app.leg.wa.gov/billsummary?BillNumber=5116&Year=2024",
    },
    {
        "id": "ct-sb-1103-2023",
        "title": "Connecticut SB 1103 — An Act Concerning Artificial Intelligence",
        "state": "CT",
        "summary": "Establishes a task force to study the use of AI in state government, including recommendations for governance, transparency, bias mitigation, and procurement standards for AI systems.",
        "full_text": "The act establishes a task force to study the use of artificial intelligence by state agencies. The task force shall make recommendations regarding governance frameworks, transparency requirements, bias mitigation standards, vendor accountability, and procurement criteria for AI systems used by state government.",
        "plain_english_summary": "Connecticut is studying how to govern AI in state government, setting the stage for future procurement and transparency requirements.",
        "status": "pending",
        "effective_date": "2025-01-01",
        "ai_category": "AI Governance / Policy",
        "industries_affected": ["government", "technology"],
        "risk_level": "low",
        "compliance_steps": [
            "Monitor task force recommendations for future compliance requirements",
            "Review current AI vendor contracts for alignment with emerging standards",
            "Participate in public comment periods if available",
        ],
        "source_url": "https://www.cga.ct.gov/2023/TOB/S/PDF/2023SB-01103-R00-SB.PDF",
    },
]


def seed():
    print("🌱 Seeding AI laws database...")
    Base.metadata.create_all(engine)

    vector_store.connect()

    with Session(engine) as session:
        added = 0
        skipped = 0
        for law_data in SEED_LAWS:
            existing = session.get(Law, law_data["id"])
            if existing:
                skipped += 1
                continue

            law = Law(**law_data)
            session.add(law)

            # Index in vector store
            try:
                embedding = embed_law(law_data["title"], law_data["summary"], law_data.get("full_text", ""))
                vector_store.upsert(
                    doc_id=law_data["id"],
                    embedding=embedding,
                    metadata={
                        "state": law_data["state"],
                        "status": law_data["status"],
                        "risk_level": law_data["risk_level"],
                        "title": law_data["title"][:200],
                    },
                )
                law.vector_indexed = True
                print(f"  ✅ {law_data['state']} — {law_data['title'][:60]}...")
                added += 1
            except Exception as e:
                print(f"  ⚠️  Vector index failed for {law_data['id']}: {e}")
                added += 1

        session.commit()

    print(f"\n✅ Done! Added {added} laws, skipped {skipped} existing.")


if __name__ == "__main__":
    seed()
