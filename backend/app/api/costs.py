from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CostItem, CostCategory, BusinessType
from app.schemas import CostItemSchema
from app.database import get_session

router = APIRouter()

@router.get("/categories")
async def get_cost_categories(session: AsyncSession = Depends(get_session)):
    """Get all cost categories"""
    result = await session.execute(
        select(CostCategory).order_by(CostCategory.order)
    )
    categories = result.scalars().all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "order": c.order
        }
        for c in categories
    ]

@router.get("/business/{business_type_id}")
async def get_business_costs(
    business_type_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get cost items for a specific business type"""

    # Verify business exists
    business_result = await session.execute(
        select(BusinessType).where(BusinessType.id == business_type_id)
    )
    business = business_result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business type not found")

    # Get cost items grouped by category
    cost_result = await session.execute(
        select(CostItem, CostCategory)
        .join(CostCategory)
        .where(CostItem.business_type_id == business_type_id)
        .order_by(CostCategory.order, CostItem.name)
    )

    items = cost_result.all()

    # Group by category
    grouped = {}
    for cost_item, category in items:
        if category.name not in grouped:
            grouped[category.name] = {
                "category_id": category.id,
                "items": []
            }
        grouped[category.name]["items"].append({
            "id": cost_item.id,
            "name": cost_item.name,
            "base_amount": cost_item.base_amount,
            "location_multiplier": cost_item.location_multiplier,
            "is_variable": cost_item.is_variable
        })

    return grouped

@router.get("/{cost_item_id}")
async def get_cost_item(
    cost_item_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get a specific cost item"""

    result = await session.execute(
        select(CostItem).where(CostItem.id == cost_item_id)
    )
    cost_item = result.scalar_one_or_none()

    if not cost_item:
        raise HTTPException(status_code=404, detail="Cost item not found")

    return {
        "id": cost_item.id,
        "name": cost_item.name,
        "description": cost_item.description,
        "base_amount": cost_item.base_amount,
        "currency": cost_item.currency,
        "location_multiplier": cost_item.location_multiplier,
        "is_variable": cost_item.is_variable
    }
