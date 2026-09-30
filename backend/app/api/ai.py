from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import Estimate, BusinessType
from app.schemas import AIInsightRequestSchema
from app.database import get_session
from app.ai_agent import estimator_agent
import json

router = APIRouter()

@router.post("/estimate")
async def get_ai_estimate(
    request: AIInsightRequestSchema,
    session: AsyncSession = Depends(get_session)
):
    """Get AI-powered cost estimation"""

    # Verify business exists
    result = await session.execute(
        select(BusinessType).where(BusinessType.id == request.business_type_id)
    )
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business type not found")

    try:
        # Get AI estimate
        estimate_data = await estimator_agent.estimate_costs(
            business_type=business.name,
            location=request.location,
            scale=request.scale,
            additional_details=request.user_inputs
        )

        return {
            "success": True,
            "data": estimate_data,
            "message": "Estimate generated successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating estimate: {str(e)}"
        )

@router.post("/save-estimate")
async def save_estimate(
    estimate_id: str,
    cost_data: dict,
    session: AsyncSession = Depends(get_session)
):
    """Save AI estimate to database"""

    # Get existing estimate
    result = await session.execute(
        select(Estimate).where(Estimate.id == estimate_id)
    )
    estimate = result.scalar_one_or_none()

    if not estimate:
        raise HTTPException(status_code=404, detail="Estimate not found")

    # Update estimate with AI data
    estimate.total_investment = cost_data.get("total_investment", 0)
    estimate.cost_breakdown = cost_data.get("cost_breakdown", {})
    estimate.ai_insights = cost_data.get("insights", "")

    await session.merge(estimate)
    await session.commit()

    return {
        "success": True,
        "estimate_id": estimate.id,
        "message": "Estimate saved successfully"
    }

@router.post("/business-plan")
async def generate_business_plan(
    request: AIInsightRequestSchema,
    session: AsyncSession = Depends(get_session)
):
    """Generate AI business plan"""

    # Verify business exists
    result = await session.execute(
        select(BusinessType).where(BusinessType.id == request.business_type_id)
    )
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business type not found")

    try:
        # First get cost estimate
        cost_estimate = await estimator_agent.estimate_costs(
            business_type=business.name,
            location=request.location,
            scale=request.scale,
            additional_details=request.user_inputs
        )

        # Generate business plan
        plan = await estimator_agent.generate_business_plan(
            business_type=business.name,
            location=request.location,
            scale=request.scale,
            cost_estimate=cost_estimate
        )

        return {
            "success": True,
            "cost_estimate": cost_estimate,
            "business_plan": plan,
            "message": "Business plan generated successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating business plan: {str(e)}"
        )

@router.get("/health")
async def health():
    """Health check for AI service"""
    return {"status": "healthy", "service": "ai-estimation"}
