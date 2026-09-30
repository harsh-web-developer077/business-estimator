from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class BusinessType(Base):
    __tablename__ = "business_types"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    category = Column(String(50))
    icon = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    cost_items = relationship("CostItem", back_populates="business_type")
    estimates = relationship("Estimate", back_populates="business_type")

class CostCategory(Base):
    __tablename__ = "cost_categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    order = Column(Integer, default=0)

    cost_items = relationship("CostItem", back_populates="category")

class CostItem(Base):
    __tablename__ = "cost_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_type_id = Column(String(36), ForeignKey("business_types.id"))
    category_id = Column(String(36), ForeignKey("cost_categories.id"))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    base_amount = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    location_multiplier = Column(Float, default=1.0)
    is_variable = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    business_type = relationship("BusinessType", back_populates="cost_items")
    category = relationship("CostCategory", back_populates="cost_items")

class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_type_id = Column(String(36), ForeignKey("business_types.id"))
    user_input = Column(JSON, nullable=False)
    total_investment = Column(Float, nullable=False)
    cost_breakdown = Column(JSON, nullable=False)
    ai_insights = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    business_type = relationship("BusinessType", back_populates="estimates")

class BusinessTemplate(Base):
    __tablename__ = "business_templates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_type_id = Column(String(36), ForeignKey("business_types.id"))
    name = Column(String(200), nullable=False)
    location = Column(String(100))
    scale = Column(String(50))
    template_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
