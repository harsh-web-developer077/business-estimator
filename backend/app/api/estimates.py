from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Estimate, BusinessType
from app.schemas import EstimateInputSchema, EstimateResponseSchema
from app.database import get_session
import json

router = APIRouter()

@router.post("/", response_model=dict)
async def create_estimate(
    estimate_input: EstimateInputSchema,
    session: AsyncSession = Depends(get_session)
):
    """Create a new cost estimate"""

    # Verify business type exists
    result = await session.execute(
        select(BusinessType).where(BusinessType.id == estimate_input.business_type_id)
    )
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business type not found")

    # Create estimate record
    estimate = Estimate(
        business_type_id=estimate_input.business_type_id,
        user_input=estimate_input.dict(),
        total_investment=0,  # Will be updated by AI
        cost_breakdown={}
    )

    session.add(estimate)
    await session.commit()
    await session.refresh(estimate)

    return {
        "id": estimate.id,
        "message": "Estimate created. Processing with AI...",
        "status": "pending"
    }

@router.get("/{estimate_id}")
async def get_estimate(
    estimate_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get estimate details"""

    result = await session.execute(
        select(Estimate).where(Estimate.id == estimate_id)
    )
    estimate = result.scalar_one_or_none()

    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")

    # Load related business type
    business_result = await session.execute(
        select(BusinessType).where(BusinessType.id == estimate.business_type_id)
    )
    business = business_result.scalar_one_or_none()

    return {
        "id": estimate.id,
        "business_type": {
            "id": business.id,
            "name": business.name,
            "description": business.description
        },
        "total_investment": estimate.total_investment,
        "cost_breakdown": estimate.cost_breakdown,
        "ai_insights": estimate.ai_insights,
        "created_at": estimate.created_at
    }

@router.get("/")
async def list_estimates(
    session: AsyncSession = Depends(get_session),
    limit: int = 10,
    offset: int = 0
):
    """List recent estimates"""

    result = await session.execute(
        select(Estimate).order_by(Estimate.created_at.desc()).limit(limit).offset(offset)
    )
    estimates = result.scalars().all()

    return {
        "total": len(estimates),
        "estimates": [
            {
                "id": e.id,
                "total_investment": e.total_investment,
                "created_at": e.created_at
            }
            for e in estimates
        ]
    }

@router.delete("/{estimate_id}")
async def delete_estimate(
    estimate_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete an estimate"""

    result = await session.execute(
        select(Estimate).where(Estimate.id == estimate_id)
    )
    estimate = result.scalar_one_or_none()

    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")

    await session.delete(estimate)
    await session.commit()

    return {"message": "Estimate deleted successfully"}
