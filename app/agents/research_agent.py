import json
from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent responsible for researching top Product Hunt launches and finding relevant hunters"""

    def __init__(self):
        super().__init__()
        self.agent_type = "research"

    def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research top launches and suggest hunters"""
        try:
            product_category = request_data.get("product_category", "")
            target_audience = request_data.get("target_audience", "")

            # Research top launches
            top_launches = self._research_top_launches(product_category)

            # Find recommended hunters
            recommended_hunters = self._find_recommended_hunters(
                product_category, target_audience
            )

            # Generate insights
            insights = self._generate_insights(top_launches, product_category)

            # Competitor analysis
            competitor_analysis = self._analyze_competitors(
                top_launches, product_category
            )

            return self.format_response(
                success=True,
                data={
                    "top_launches": top_launches,
                    "recommended_hunters": recommended_hunters,
                    "insights": insights,
                    "competitor_analysis": competitor_analysis,
                },
            )

        except Exception as e:
            return self.format_response(
                success=False, error=f"Research failed: {str(e)}"
            )

    def _research_top_launches(self, product_category: str) -> List[Dict[str, Any]]:
        """Research top Product Hunt launches in the category"""

        # For hackathon demo, we'll use mock data and LLM-generated insights
        prompt = f"""
Research and analyze the top 5 Product Hunt launches in the "{product_category}" category from the past 6 months.

For each launch, provide:
- Product name and tagline
- Launch date
- Final ranking/position
- Key success factors
- What made them stand out
- Lessons learned

Focus on products that achieved top 5 daily rankings.

Format as JSON:
{{
    "launches": [
        {{
            "name": "Product Name",
            "tagline": "Product tagline",
            "launch_date": "2024-XX-XX",
            "ranking": "1st place",
            "success_factors": ["Factor 1", "Factor 2"],
            "standout_features": "What made it unique",
            "lessons": "Key takeaways"
        }}
    ]
}}
"""

        response = self.invoke_llm(prompt, max_tokens=4000)

        try:
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("launches", [])
        except BaseException:
            pass

        # Fallback mock data
        return [
            {
                "name": f"Top {product_category} Tool",
                "tagline": "Revolutionary solution for modern teams",
                "launch_date": "2024-10-15",
                "ranking": "1st place",
                "success_factors": [
                    "Strong community",
                    "Clear value prop",
                    "Great timing",
                ],
                "standout_features": "Unique approach to common problem",
                "lessons": "Focus on user experience and community building",
            },
            {
                "name": f"AI-Powered {product_category}",
                "tagline": "Automate your workflow with AI",
                "launch_date": "2024-09-20",
                "ranking": "2nd place",
                "success_factors": ["AI trend", "Clear demo", "Founder story"],
                "standout_features": "First to market with AI integration",
                "lessons": "Timing and trend alignment crucial",
            },
        ]

    def _find_recommended_hunters(
        self, product_category: str, target_audience: str
    ) -> List[Dict[str, Any]]:
        """Find recommended Product Hunt hunters"""

        prompt = f"""
Find 5 recommended Product Hunt hunters for a product in the "{product_category}" category targeting "{target_audience}".

For each hunter, provide:
- Name and @handle
- Specialization/niche
- Follower count (estimated)
- Success rate with similar products
- Contact approach
- Why they're a good fit

Focus on hunters who:
- Have experience with {product_category} products
- Have good engagement rates
- Are active in the community
- Have helped similar products succeed

Format as JSON:
{{
    "hunters": [
        {{
            "name": "Hunter Name",
            "handle": "@hunterhandle",
            "specialization": "AI/Productivity tools",
            "followers": "10K+",
            "success_rate": "High",
            "contact_approach": "Twitter DM",
            "why_fit": "Has helped 3 AI tools reach #1"
        }}
    ]
}}
"""

        response = self.invoke_llm(prompt, max_tokens=3000)

        try:
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("hunters", [])
        except BaseException:
            pass

        # Fallback mock data
        return [
            {
                "name": "Tech Hunter",
                "handle": "@techhunter",
                "specialization": f"{product_category} and productivity tools",
                "followers": "15K+",
                "success_rate": "High",
                "contact_approach": "Twitter DM or email",
                "why_fit": f"Specializes in {product_category} launches",
            },
            {
                "name": "Startup Advocate",
                "handle": "@startupadvocate",
                "specialization": "Early-stage products",
                "followers": "8K+",
                "success_rate": "Medium-High",
                "contact_approach": "LinkedIn message",
                "why_fit": "Great at helping new founders",
            },
        ]

    def _generate_insights(
        self, top_launches: List[Dict[str, Any]], product_category: str
    ) -> List[str]:
        """Generate insights from top launches"""

        prompt = f"""
Based on the top launches in the "{product_category}" category, generate 5 key insights for launching a new product.

Analyze patterns in:
- Success factors
- Common mistakes
- Timing strategies
- Community building
- Marketing approaches

Make insights actionable and specific to this category.

Format as a simple list of insights.
"""

        response = self.invoke_llm(prompt, max_tokens=2000)

        # Extract insights from response
        insights = []
        lines = response.split("\n")
        for line in lines:
            line = line.strip()
            if line and (
                line.startswith("-") or line.startswith("•") or line[0].isdigit()
            ):
                insights.append(line)

        return (
            insights[:5]
            if insights
            else [
                f"Products in {product_category} that launch on Tuesdays perform 20% better",
                "Community building 2-3 weeks before launch is crucial for success",
                "Clear, benefit-focused taglines outperform feature-focused ones",
                "Founder stories and behind-the-scenes content drive engagement",
                "Posting updates and responding to comments increases visibility",
            ]
        )

    def _analyze_competitors(
        self, top_launches: List[Dict[str, Any]], product_category: str
    ) -> Dict[str, Any]:
        """Analyze competitors and market positioning"""

        prompt = f"""
Analyze the competitive landscape for the "{product_category}" category based on recent Product Hunt launches.

Provide:
- Market saturation level
- Common pricing strategies
- Key differentiators that work
- Gaps in the market
- Recommended positioning strategy

Format as JSON:
{{
    "market_saturation": "Low/Medium/High",
    "pricing_strategies": ["Strategy 1", "Strategy 2"],
    "key_differentiators": ["Differentiator 1", "Differentiator 2"],
    "market_gaps": ["Gap 1", "Gap 2"],
    "positioning_strategy": "Recommended approach"
}}
"""

        response = self.invoke_llm(prompt, max_tokens=2000)

        try:
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data
        except BaseException:
            pass

        # Fallback analysis
        return {
            "market_saturation": "Medium",
            "pricing_strategies": ["Freemium", "One-time purchase", "Subscription"],
            "key_differentiators": [
                "User experience",
                "AI integration",
                "Community features",
            ],
            "market_gaps": [
                "Better onboarding",
                "Mobile-first approach",
                "Enterprise features",
            ],
            "positioning_strategy": "Focus on unique value proposition and user experience",
        }
