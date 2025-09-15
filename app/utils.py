import json
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict

import boto3


class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-west-2")
        )
        self.model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        self.temperature = 0.3

    def invoke_model(self, prompt: str, max_tokens: int = 4000) -> str:
        """Invoke Claude 3.7 Sonnet via Bedrock"""
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": self.temperature,
                "messages": [{"role": "user", "content": prompt}],
            }

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType="application/json",
            )

            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]

        except Exception as e:
            error_msg = str(e)
            if "ValidationException" in error_msg:
                raise Exception(
                    f"Model validation error: {error_msg}\n"
                    f"Make sure the model '{self.model_id}' is available in your region.\n"
                    f"Check AWS Bedrock console for available models.\n"
                    f"Region: {os.getenv('AWS_REGION', 'us-west-2')}"
                )
            elif "AccessDeniedException" in error_msg:
                raise Exception(
                    f"Access denied: {error_msg}\n"
                    f"Make sure your AWS credentials have Bedrock permissions."
                )
            else:
                raise Exception(f"Bedrock API error: {error_msg}")


def parse_launch_date(date_input: str) -> datetime:
    """Parse natural language date input"""
    from dateutil import parser

    # Handle relative dates
    if "next" in date_input.lower():
        if "tuesday" in date_input.lower():
            today = datetime.now()
            days_ahead = 1 - today.weekday()  # Tuesday is 1
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif "friday" in date_input.lower():
            today = datetime.now()
            days_ahead = 4 - today.weekday()  # Friday is 4
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return today + timedelta(days=days_ahead)

    # Try parsing with dateutil
    try:
        return parser.parse(date_input)
    except Exception:
        # Fallback to adding days if it's a number
        if date_input.isdigit():
            return datetime.now() + timedelta(days=int(date_input))
        raise ValueError(f"Could not parse date: {date_input}")


def calculate_timeline_days(launch_date: datetime) -> int:
    """Calculate days from now to launch date"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    launch = launch_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return (launch - today).days


def format_date_for_display(date: datetime) -> str:
    """Format date for user-friendly display"""
    return date.strftime("%A, %B %d, %Y")


def clean_text(text: str) -> str:
    """Clean and format text output"""
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text.strip())
    # Remove markdown formatting if present
    text = re.sub(r"[*_`]", "", text)
    return text


def extract_json_from_response(response: str) -> Dict[str, Any]:
    """Extract JSON from AI response"""
    try:
        # Look for JSON in the response
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            # If no JSON found, return the response as text
            return {"content": response}
    except json.JSONDecodeError:
        return {"content": response}
