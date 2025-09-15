from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProductInfo(BaseModel):
    name: str
    description: str
    category: str
    target_audience: str
    launch_date: Optional[str] = None


class PlanningRequest(BaseModel):
    product_name: str
    product_type: str
    launch_date: str
    additional_notes: Optional[str] = None


class PlanningResponse(BaseModel):
    timeline: List[Dict[str, Any]]
    total_days: int
    launch_date: str
    key_milestones: List[str]


class AssetPrepRequest(BaseModel):
    product_name: str
    elevator_pitch: str
    target_audience: str
    tone: Optional[str] = "professional"


class AssetPrepResponse(BaseModel):
    taglines: List[str]
    short_description: str
    tweets: List[str]
    suggestions: List[str]


class ResearchRequest(BaseModel):
    product_category: str
    target_audience: str
    budget_range: Optional[str] = None


class ResearchResponse(BaseModel):
    top_launches: List[Dict[str, Any]]
    recommended_hunters: List[Dict[str, Any]]
    insights: List[str]
    competitor_analysis: Dict[str, Any]


class AgentResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    agent_type: str
