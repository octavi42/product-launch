from typing import Any, Dict

from app.agents.asset_prep_agent import AssetPrepAgent
from app.agents.planning_agent import PlanningAgent
from app.agents.research_agent import ResearchAgent
from app.models import AgentResponse


class AgentCoordinator:
    """Coordinates all Product Hunt agents"""

    def __init__(self):
        self.planning_agent = PlanningAgent()
        self.asset_prep_agent = AssetPrepAgent()
        self.research_agent = ResearchAgent()

    def route_request(
        self, agent_type: str, request_data: Dict[str, Any]
    ) -> AgentResponse:
        """Route request to appropriate agent"""

        try:
            if agent_type == "planning":
                result = self.planning_agent.process(request_data)
            elif agent_type == "asset_prep":
                result = self.asset_prep_agent.process(request_data)
            elif agent_type == "research":
                result = self.research_agent.process(request_data)
            else:
                return AgentResponse(
                    success=False,
                    error=f"Unknown agent type: {agent_type}",
                    agent_type=agent_type,
                )

            return AgentResponse(
                success=result["success"],
                data=result.get("data"),
                error=result.get("error"),
                agent_type=agent_type,
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Agent execution failed: {str(e)}",
                agent_type=agent_type,
            )

    def get_available_agents(self) -> Dict[str, str]:
        """Get list of available agents and their descriptions"""
        return {
            "planning": "Generate launch timeline and checklist",
            "asset_prep": "Create taglines, descriptions, and tweets",
            "research": "Find top launches and recommend hunters",
        }
