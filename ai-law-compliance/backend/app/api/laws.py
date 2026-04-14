from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from app.db.database import get_db
from app.models.law import Law, LawStatus as DBLawStatus
from app.schemas.law import LawRead, LawListItem

router = APIRouter(prefix="/api/laws", tags=["Laws"])


@router.get("", response_model=List[LawListItem])
async def list_laws(
    state: Optional[str] = Query(None, min_length=2, max_length=2),
    status: Optional[str] = None,
    risk_level: Optional[str] = None,
    ai_category: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List AI laws with optional filters."""
    filters = [Law.is_ai_relevant == True]
    if state:
        filters.append(Law.state == state.upper())
    if status:
        filters.append(Law.status == status)
    if risk_level:
        filters.append(Law.risk_level == risk_level)
    if ai_category:
        filters.append(Law.ai_category.ilike(f"%{ai_category}%"))

    result = await db.execute(
        select(Law).where(and_(*filters)).offset(offset).limit(limit)
    )
    return result.scalars().all()


@router.get("/state/{state}", response_model=List[LawListItem])
async def laws_by_state(state: str, db: AsyncSession = Depends(get_db)):
    """Get all AI laws for a specific state."""
    result = await db.execute(
        select(Law).where(
            and_(Law.state == state.upper(), Law.is_ai_relevant == True)
        )
    )
    return result.scalars().all()


@router.get("/{law_id}", response_model=LawRead)
async def get_law(law_id: str, db: AsyncSession = Depends(get_db)):
    """Get full details for a specific law."""
    result = await db.execute(select(Law).where(Law.id == law_id))
    law = result.scalar_one_or_none()
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law
