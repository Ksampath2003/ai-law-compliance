import uuid
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.vector_store import vector_store
from app.models.law import Law
from app.schemas.law import IngestRequest, IngestResponse
from app.services.ai_filter import is_ai_relevant
from app.services.embeddings import embed_law
from app.services.compliance import generate_plain_english_summary
from app.core.security import require_admin

router = APIRouter(prefix="/api/ingest", tags=["Ingest"])


@router.post("", response_model=IngestResponse, dependencies=[Security(require_admin)])
async def ingest_laws(
    request: IngestRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Ingest new laws into the system (admin only).
    Optionally run AI relevance filtering and generate plain-English summaries.
    """
    processed = 0
    accepted = 0
    rejected = 0
    errors = []

    for law_data in request.laws:
        processed += 1
        try:
            # AI relevance filter
            if request.run_ai_filter:
                relevant, method = is_ai_relevant(
                    law_data.title,
                    law_data.summary,
                    law_data.full_text or "",
                )
                if not relevant:
                    rejected += 1
                    continue

            # Assign ID if missing
            law_id = law_data.id or str(uuid.uuid4())

            # Check if already exists
            existing = await db.execute(select(Law).where(Law.id == law_id))
            law = existing.scalar_one_or_none()

            plain_summary = None
            if request.generate_summaries and law_data.full_text:
                plain_summary = generate_plain_english_summary(
                    law_data.title, law_data.full_text
                )

            if law:
                # Update existing
                for field, value in law_data.model_dump(exclude={"id"}, exclude_none=True).items():
                    setattr(law, field, value)
                if plain_summary:
                    law.plain_english_summary = plain_summary
            else:
                # Create new
                law = Law(
                    id=law_id,
                    **law_data.model_dump(exclude={"id"}, exclude_none=True),
                    plain_english_summary=plain_summary,
                    is_ai_relevant=True,
                )
                db.add(law)

            await db.flush()

            # Index in vector store
            embedding = embed_law(law_data.title, law_data.summary, law_data.full_text or "")
            vector_store.upsert(
                doc_id=law_id,
                embedding=embedding,
                metadata={
                    "state": law_data.state,
                    "status": law_data.status.value if law_data.status else "pending",
                    "risk_level": law_data.risk_level.value if law_data.risk_level else "medium",
                    "title": law_data.title[:200],
                },
            )
            law.vector_indexed = True
            accepted += 1

        except Exception as e:
            errors.append(f"Error processing '{law_data.title}': {str(e)}")
            rejected += 1

    await db.commit()

    return IngestResponse(
        processed=processed,
        accepted=accepted,
        rejected=rejected,
        errors=errors,
    )
