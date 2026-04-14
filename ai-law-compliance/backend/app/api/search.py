from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.vector_store import vector_store
from app.models.law import Law
from app.schemas.law import SearchRequest, SearchResponse, SearchResult, LawListItem
from app.services.embeddings import embed_text

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.post("", response_model=SearchResponse)
async def semantic_search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Semantic search across all AI laws.
    Describe your situation and find relevant legislation.
    """
    # Embed query
    query_embedding = embed_text(request.query)

    # Build vector store filters
    filters = None
    if request.state or request.status or request.risk_level:
        filters = {}
        if request.state:
            filters["state"] = request.state.upper()
        if request.status:
            filters["status"] = request.status.value
        if request.risk_level:
            filters["risk_level"] = request.risk_level.value

    # Query vector store
    try:
        vector_results = vector_store.query(query_embedding, top_k=request.top_k, filters=filters)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Vector store error: {str(e)}")

    if not vector_results:
        return SearchResponse(results=[], total=0)

    # Fetch full law records from DB
    law_ids = [r["id"] for r in vector_results]
    scores = {r["id"]: r["score"] for r in vector_results}

    result = await db.execute(select(Law).where(Law.id.in_(law_ids)))
    laws = {law.id: law for law in result.scalars().all()}

    search_results = []
    for law_id in law_ids:
        if law_id in laws:
            search_results.append(
                SearchResult(
                    law=LawListItem.model_validate(laws[law_id]),
                    score=round(scores[law_id], 4),
                )
            )

    return SearchResponse(results=search_results, total=len(search_results))
