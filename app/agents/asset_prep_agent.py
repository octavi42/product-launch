from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.utils import clean_text


class AssetPrepAgent(BaseAgent):
    """Agent responsible for generating marketing assets like taglines, descriptions, and tweets"""

    def __init__(self):
        super().__init__()
        self.agent_type = "asset_prep"

    def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate marketing assets for Product Hunt launch"""
        try:
            product_name = request_data.get("product_name", "")
            elevator_pitch = request_data.get("elevator_pitch", "")
            target_audience = request_data.get("target_audience", "")
            tone = request_data.get("tone", "professional")

            # Generate all assets
            taglines = self._generate_taglines(
                product_name, elevator_pitch, target_audience, tone
            )
            short_description = self._generate_description(
                product_name, elevator_pitch, target_audience, tone
            )
            tweets = self._generate_tweets(
                product_name, elevator_pitch, target_audience, tone
            )
            suggestions = self._generate_suggestions(product_name, target_audience)

            return self.format_response(
                success=True,
                data={
                    "taglines": taglines,
                    "short_description": short_description,
                    "tweets": tweets,
                    "suggestions": suggestions,
                },
            )

        except Exception as e:
            return self.format_response(
                success=False, error=f"Asset generation failed: {str(e)}"
            )

    def _generate_taglines(
        self, product_name: str, elevator_pitch: str, target_audience: str, tone: str
    ) -> List[str]:
        """Generate multiple tagline options"""

        prompt = f"""
Create 5 compelling taglines for "{product_name}" for Product Hunt launch.

Product: {product_name}
Elevator pitch: {elevator_pitch}
Target audience: {target_audience}
Tone: {tone}

Requirements:
- Each tagline should be 3-8 words
- Include emotional hooks and benefits
- Make them memorable and shareable
- Vary the approach (problem-focused, benefit-focused, feature-focused, etc.)
- Ensure they work well for Product Hunt's format

Format as JSON:
{{
    "taglines": [
        "Tagline 1",
        "Tagline 2",
        "Tagline 3",
        "Tagline 4",
        "Tagline 5"
    ]
}}
"""

        response = self.invoke_llm(prompt, max_tokens=2000)

        try:
            import json
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return [clean_text(tagline) for tagline in data.get("taglines", [])]
        except BaseException:
            pass

        # Fallback taglines
        return [
            f"{product_name} - {elevator_pitch[:50]}...",
            f"Revolutionary {product_name} for {target_audience}",
            f"Transform your workflow with {product_name}",
            f"The future of {product_name} is here",
            f"Build better with {product_name}",
        ]

    def _generate_description(
        self, product_name: str, elevator_pitch: str, target_audience: str, tone: str
    ) -> str:
        """Generate short description for Product Hunt"""

        prompt = f"""
Write a compelling short description for "{product_name}" for Product Hunt launch.

Product: {product_name}
Elevator pitch: {elevator_pitch}
Target audience: {target_audience}
Tone: {tone}

Requirements:
- 2-3 sentences maximum
- Lead with the main benefit
- Include what makes it unique
- End with a call to action
- Keep it under 200 characters
- Make it scannable and engaging

Focus on the value proposition and why people should care.
"""

        response = self.invoke_llm(prompt, max_tokens=1000)
        return clean_text(response)

    def _generate_tweets(
        self, product_name: str, elevator_pitch: str, target_audience: str, tone: str
    ) -> List[str]:
        """Generate tweet variations for launch day"""

        prompt = f"""
Create 3 different tweets for launching "{product_name}" on Product Hunt.

Product: {product_name}
Elevator pitch: {elevator_pitch}
Target audience: {target_audience}
Tone: {tone}

Requirements:
- Each tweet should be under 280 characters
- Include relevant hashtags (#ProductHunt, #Launch, etc.)
- Vary the approach (announcement, behind-the-scenes, community ask)
- Include a call to action
- Make them engaging and shareable

Format as JSON:
{{
    "tweets": [
        "Tweet 1 with hashtags",
        "Tweet 2 with hashtags",
        "Tweet 3 with hashtags"
    ]
}}
"""

        response = self.invoke_llm(prompt, max_tokens=2000)

        try:
            import json
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return [clean_text(tweet) for tweet in data.get("tweets", [])]
        except BaseException:
            pass

        # Fallback tweets
        return [
            f"🚀 Just launched {product_name} on @ProductHunt! {elevator_pitch[:100]}... #ProductHunt #Launch",
            f"Excited to share {product_name} with the world! Built for {target_audience}. Check it out: #ProductHunt #Launch",
            f"After months of building, {product_name} is live on @ProductHunt! Would love your support 🙏 #ProductHunt #Launch",
        ]

    def _generate_suggestions(
        self, product_name: str, target_audience: str
    ) -> List[str]:
        """Generate additional suggestions for the launch"""

        prompt = f"""
Provide 5 actionable suggestions for launching "{product_name}" on Product Hunt.

Product: {product_name}
Target audience: {target_audience}

Focus on:
- Timing and strategy
- Community building
- Content creation
- Networking
- Post-launch activities

Make suggestions specific and actionable for a founder.
"""

        response = self.invoke_llm(prompt, max_tokens=1500)

        # Extract suggestions from response
        suggestions = []
        lines = response.split("\n")
        for line in lines:
            line = clean_text(line)
            if line and (
                line.startswith("-") or line.startswith("•") or line[0].isdigit()
            ):
                suggestions.append(line)

        return (
            suggestions[:5]
            if suggestions
            else [
                f"Start building your community around {product_name} 2-3 weeks before launch",
                f"Create a demo video showcasing {product_name}'s key features",
                f"Reach out to {target_audience} influencers and thought leaders",
                "Prepare social media content for launch day and the following week",
                "Plan follow-up activities to maintain momentum after launch day",
            ]
        )
