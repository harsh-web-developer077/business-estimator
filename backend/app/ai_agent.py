from anthropic import Anthropic
from app.config import settings
from typing import Dict, List, Any
import json

client = Anthropic()

class BusinessEstimatorAgent:
    """Multi-agent system for intelligent business cost estimation"""

    def __init__(self):
        self.model = settings.claude_model
        self.api_key = settings.claude_api_key

    async def estimate_costs(
        self,
        business_type: str,
        location: str,
        scale: str,
        additional_details: Dict
    ) -> Dict[str, Any]:
        """
        Use Claude to estimate business costs with market research context
        """

        prompt = f"""You are an expert business consultant analyzing startup costs.

Business Type: {business_type}
Location: {location}
Scale: {scale} (small: <25 employees, medium: 25-100, large: >100)
Additional Details: {json.dumps(additional_details, indent=2)}

Provide a detailed cost breakdown in JSON format with:
1. Initial Setup Costs (license, permits, infrastructure, equipment)
2. Inventory & Materials
3. Staffing (first year salaries/wages)
4. Marketing & Launch
5. Professional Services (legal, accounting)
6. Working Capital Reserve

For each category, provide:
- item_name: str
- estimated_cost: float (in INR)
- notes: str
- location_adjustment: float (1.0 = base, 1.5 = 50% more expensive)

Also provide:
- total_investment: float
- monthly_operating_costs: float
- breakeven_months: int
- key_risks: list of strings
- funding_recommendations: dict with loan/grant/equity suggestions
- success_factors: list of critical success factors
- cost_saving_opportunities: list of strings

Return ONLY valid JSON, no markdown."""

        message = client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Parse JSON from response
        try:
            cost_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            cost_data = self._generate_fallback_estimate(business_type, location, scale)

        return cost_data

    async def generate_business_plan(
        self,
        business_type: str,
        location: str,
        scale: str,
        cost_estimate: Dict
    ) -> str:
        """
        Generate business plan recommendations
        """

        prompt = f"""As a business strategist, create a concise business plan for:

Business: {business_type}
Location: {location}
Scale: {scale}
Estimated Investment: ₹{cost_estimate.get('total_investment', 0):,.0f}

Provide:
1. Executive Summary (100 words)
2. Market Analysis (location-specific insights)
3. Operational Plan (first 12 months)
4. Marketing Strategy
5. Financial Projections
6. Key Milestones
7. Critical Success Factors

Keep response under 1000 words, practical and actionable."""

        message = client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    def _generate_fallback_estimate(self, business_type: str, location: str, scale: str) -> Dict:
        """Fallback estimates if AI call fails"""

        base_estimates = {
            "cafe": {
                "small": 25_00_000,  # 25 lakhs
                "medium": 50_00_000,
                "large": 100_00_000
            },
            "salon": {
                "small": 10_00_000,  # 10 lakhs
                "medium": 25_00_000,
                "large": 50_00_000
            },
            "retail": {
                "small": 20_00_000,  # 20 lakhs
                "medium": 50_00_000,
                "large": 150_00_000
            },
            "fitness": {
                "small": 20_00_000,
                "medium": 50_00_000,
                "large": 150_00_000
            },
            "coworking": {
                "small": 50_00_000,
                "medium": 150_00_000,
                "large": 500_00_000
            }
        }

        business_key = business_type.lower()
        scale_key = scale.lower()

        base_amount = base_estimates.get(business_key, {}).get(scale_key, 20_00_000)

        return {
            "total_investment": base_amount,
            "monthly_operating_costs": base_amount * 0.1,
            "breakeven_months": 24,
            "cost_breakdown": {
                "setup": base_amount * 0.3,
                "inventory": base_amount * 0.3,
                "staffing": base_amount * 0.2,
                "marketing": base_amount * 0.1,
                "reserve": base_amount * 0.1
            },
            "funding_recommendations": {
                "personal_savings": base_amount * 0.3,
                "bank_loan": base_amount * 0.5,
                "investors": base_amount * 0.2
            }
        }

# Global instance
estimator_agent = BusinessEstimatorAgent()
