from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class CostCategorySchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    order: int = 0

class CostItemSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    base_amount: float
    currency: str = "INR"
    location_multiplier: float = 1.0
    is_variable: bool = False
    category: CostCategorySchema

class BusinessTypeSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None

class BusinessTypeDetailSchema(BusinessTypeSchema):
    cost_items: List[CostItemSchema] = []

class EstimateInputSchema(BaseModel):
    business_type_id: str
    location: str
    scale: str  # small, medium, large
    additional_details: Dict = {}

class CostBreakdownSchema(BaseModel):
    category: str
    items: List[Dict]
    subtotal: float

class EstimateResponseSchema(BaseModel):
    id: str
    business_type: BusinessTypeSchema
    total_investment: float
    cost_breakdown: List[CostBreakdownSchema]
    ai_insights: Optional[str] = None
    funding_suggestions: Optional[Dict] = None
    created_at: datetime

class AIInsightRequestSchema(BaseModel):
    business_type_id: str
    location: str
    scale: str
    user_inputs: Dict

class AIInsightResponseSchema(BaseModel):
    cost_estimate: float
    breakdown: Dict
    insights: str
    recommendations: List[str]
    risks: List[str]
    funding_options: Dict
