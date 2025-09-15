import json
from abc import ABC, abstractmethod
from typing import Any, Dict

from app.utils import BedrockClient


class BaseAgent(ABC):
    """Base class for all Product Hunt agents"""

    def __init__(self):
        self.bedrock = BedrockClient()
        self.agent_type = self.__class__.__name__.lower().replace("agent", "")

    @abstractmethod
    def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the request and return response"""
        pass

    def invoke_llm(self, prompt: str, max_tokens: int = 4000) -> str:
        """Invoke the language model with the given prompt"""
        try:
            return self.bedrock.invoke_model(prompt, max_tokens)
        except Exception as e:
            raise Exception(f"LLM invocation failed: {str(e)}")

    def format_response(
        self, success: bool, data: Any = None, error: str = None
    ) -> Dict[str, Any]:
        """Format the agent response"""
        return {
            "success": success,
            "data": data,
            "error": error,
            "agent_type": self.agent_type,
        }

    def extract_structured_data(
        self, response: str, expected_keys: list
    ) -> Dict[str, Any]:
        """Extract structured data from LLM response"""
        try:
            # Try to find JSON in the response
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # Validate that expected keys are present
                for key in expected_keys:
                    if key not in data:
                        data[key] = None
                return data
            else:
                # Fallback: create structure from text
                return {key: response for key in expected_keys}
        except json.JSONDecodeError:
            return {key: response for key in expected_keys}
