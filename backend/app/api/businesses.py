from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import BusinessType, CostItem, CostCategory
from app.schemas import BusinessTypeSchema, BusinessTypeDetailSchema
from app.database import get_session

router = APIRouter()

SEED_BUSINESSES = [
    {
        "name": "Cafe",
        "description": "Coffee shop or casual dining cafe",
        "category": "Food & Beverage",
        "icon": "☕"
    },
    {
        "name": "Salon",
        "description": "Hair and beauty salon",
        "category": "Services",
        "icon": "💇"
    },
    {
        "name": "Retail Shop",
        "description": "General retail store",
        "category": "Retail",
        "icon": "🛍️"
    },
    {
        "name": "Fitness Studio",
        "description": "Gym or fitness center",
        "category": "Health & Wellness",
        "icon": "💪"
    },
    {
        "name": "Co-working Space",
        "description": "Shared office space",
        "category": "Services",
        "icon": "💼"
    }
]

@router.get("/", response_model=list[BusinessTypeSchema])
async def list_businesses(session: AsyncSession = Depends(get_session)):
    """Get all business types"""
    result = await session.execute(select(BusinessType))
    businesses = result.scalars().all()

    if not businesses:
        # Seed initial data
        for business_data in SEED_BUSINESSES:
            business = BusinessType(**business_data)
            session.add(business)
        await session.commit()
        result = await session.execute(select(BusinessType))
        businesses = result.scalars().all()

    return businesses

@router.get("/{business_id}", response_model=BusinessTypeDetailSchema)
async def get_business(business_id: str, session: AsyncSession = Depends(get_session)):
    """Get business type with cost items"""
    result = await session.execute(
        select(BusinessType).where(BusinessType.id == business_id)
    )
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business type not found")

    # Load cost items
    cost_result = await session.execute(
        select(CostItem).where(CostItem.business_type_id == business_id)
    )
    cost_items = cost_result.scalars().all()

    return business

@router.post("/seed")
async def seed_businesses(session: AsyncSession = Depends(get_session)):
    """Seed initial business types and cost categories"""

    # Create categories
    categories_data = [
        {"name": "Setup & Infrastructure", "order": 1},
        {"name": "Inventory & Materials", "order": 2},
        {"name": "Staffing & Training", "order": 3},
        {"name": "Marketing & Launch", "order": 4},
        {"name": "Professional Services", "order": 5},
        {"name": "Working Capital", "order": 6},
    ]

    categories = {}
    for cat_data in categories_data:
        category = CostCategory(**cat_data)
        session.add(category)
        await session.flush()
        categories[cat_data["name"]] = category.id

    # Create business types
    for business_data in SEED_BUSINESSES:
        business = BusinessType(**business_data)
        session.add(business)
        await session.flush()

    await session.commit()

    return {
        "message": "Database seeded successfully",
        "businesses": len(SEED_BUSINESSES),
        "categories": len(categories)
    }
