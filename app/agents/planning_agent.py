from datetime import datetime
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.utils import (
    calculate_timeline_days,
    format_date_for_display,
    parse_launch_date,
)


class PlanningAgent(BaseAgent):
    """Agent responsible for generating launch timelines and checklists"""

    def __init__(self):
        super().__init__()
        self.agent_type = "planning"

    def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive launch timeline"""
        try:
            product_name = request_data.get("product_name", "")
            product_type = request_data.get("product_type", "")
            launch_date_input = request_data.get("launch_date", "")
            additional_notes = request_data.get("additional_notes", "")

            # Parse launch date
            launch_date = parse_launch_date(launch_date_input)
            days_until_launch = calculate_timeline_days(launch_date)

            if days_until_launch < 0:
                return self.format_response(
                    success=False,
                    error="Launch date is in the past. Please provide a future date.",
                )

            # Generate timeline
            timeline = self._generate_timeline(
                product_name,
                product_type,
                launch_date,
                days_until_launch,
                additional_notes,
            )

            # Extract key milestones
            key_milestones = self._extract_milestones(timeline)

            return self.format_response(
                success=True,
                data={
                    "timeline": timeline,
                    "total_days": days_until_launch,
                    "launch_date": format_date_for_display(launch_date),
                    "key_milestones": key_milestones,
                },
            )

        except Exception as e:
            return self.format_response(
                success=False, error=f"Planning failed: {str(e)}"
            )

    def _generate_timeline(
        self,
        product_name: str,
        product_type: str,
        launch_date: datetime,
        days_until_launch: int,
        additional_notes: str,
    ) -> list:
        """Generate detailed timeline using LLM"""

        prompt = f"""
You are a Product Hunt launch expert. Generate a detailed timeline for launching "{product_name}" (a {product_type}) on {format_date_for_display(launch_date)}.

Current date: {datetime.now().strftime("%A, %B %d, %Y")}
Days until launch: {days_until_launch}

Additional context: {additional_notes}

Create a comprehensive timeline with specific tasks, deadlines, and priorities. Include:
1. Pre-launch preparation (weeks before)
2. Final preparation (days before)
3. Launch day activities
4. Post-launch follow-up

For each task, provide:
- Task name
- Due date (relative to launch)
- Priority (High/Medium/Low)
- Estimated time needed
- Dependencies
- Success criteria

Format as JSON with this structure:
{{
    "timeline": [
        {{
            "phase": "Pre-launch (2-3 weeks before)",
            "tasks": [
                {{
                    "name": "Task name",
                    "due_date": "X days before launch",
                    "priority": "High",
                    "time_estimate": "2-3 hours",
                    "dependencies": "Previous task",
                    "success_criteria": "What success looks like"
                }}
            ]
        }}
    ]
}}

Focus on actionable, specific tasks that founders can execute immediately.
"""

        response = self.invoke_llm(prompt, max_tokens=6000)

        # Extract JSON from response
        try:
            import json
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("timeline", [])
            else:
                # Fallback: create basic timeline
                return self._create_fallback_timeline(days_until_launch)
        except BaseException:
            return self._create_fallback_timeline(days_until_launch)

    def _create_fallback_timeline(self, days_until_launch: int) -> list:
        """Create a basic timeline if LLM fails"""
        timeline = []

        if days_until_launch >= 14:
            timeline.append({"phase": "Pre-launch (2+ weeks before)",
                             "tasks": [{"name": "Create Product Hunt account and profile",
                                        "due_date": f"{days_until_launch - 14} days before launch",
                                        "priority": "High",
                                        "time_estimate": "1 hour",
                                        "dependencies": "None",
                                        "success_criteria": "Account created with complete profile",
                                        },
                                       {"name": "Prepare product assets (logo, screenshots, demo video)",
                                        "due_date": f"{days_until_launch - 10} days before launch",
                                        "priority": "High",
                                        "time_estimate": "4-6 hours",
                                        "dependencies": "None",
                                        "success_criteria": "All visual assets ready",
                                        },
                                       ],
                             })

        if days_until_launch >= 7:
            timeline.append(
                {
                    "phase": "Final preparation (1 week before)",
                    "tasks": [
                        {
                            "name": "Write compelling product description and tagline",
                            "due_date": f"{days_until_launch - 7} days before launch",
                            "priority": "High",
                            "time_estimate": "2-3 hours",
                            "dependencies": "Product assets ready",
                            "success_criteria": "Description approved and ready",
                        },
                        {
                            "name": "Identify and reach out to potential hunters",
                            "due_date": f"{days_until_launch - 5} days before launch",
                            "priority": "High",
                            "time_estimate": "3-4 hours",
                            "dependencies": "None",
                            "success_criteria": "At least 3 hunters confirmed",
                        },
                    ],
                }
            )

        timeline.append(
            {
                "phase": "Launch day",
                "tasks": [
                    {
                        "name": "Submit product to Product Hunt",
                        "due_date": "Launch day (12:01 AM PST)",
                        "priority": "High",
                        "time_estimate": "30 minutes",
                        "dependencies": "All assets and hunters ready",
                        "success_criteria": "Product live on Product Hunt",
                    },
                    {
                        "name": "Share on social media and personal networks",
                        "due_date": "Launch day (morning)",
                        "priority": "High",
                        "time_estimate": "2-3 hours",
                        "dependencies": "Product live",
                        "success_criteria": "Initial momentum generated",
                    },
                ],
            }
        )

        return timeline

    def _extract_milestones(self, timeline: list) -> list:
        """Extract key milestones from timeline"""
        milestones = []
        for phase in timeline:
            for task in phase.get("tasks", []):
                if task.get("priority") == "High":
                    milestones.append(f"{task['name']} - {task['due_date']}")
        return milestones[:5]  # Top 5 milestones
