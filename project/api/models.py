"""Pydantic models for API requests and responses."""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ProductRequest(BaseModel):
    """Request model for product launch assistance."""
    product_name: str
    product_description: str
    product_type: str = "SaaS"
    target_audience: str = ""
    launch_date: str = ""
    additional_notes: str = ""
    github_repo: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    """Request model for chat interaction."""
    message: str
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        # Allow extra fields to be ignored instead of causing validation errors
        extra = "ignore"


class AgentResponse(BaseModel):
    """Response model for agent interactions."""
    success: bool
    response: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TimelineResponse(BaseModel):
    """Response model for launch timeline."""
    success: bool
    timeline: Optional[List[Dict[str, Any]]] = None
    total_days: Optional[int] = None
    launch_date: Optional[str] = None
    key_milestones: Optional[List[str]] = None
    error: Optional[str] = None


class MarketingAssetsResponse(BaseModel):
    """Response model for marketing assets."""
    success: bool
    taglines: Optional[List[str]] = None
    short_description: Optional[str] = None
    tweets: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    error: Optional[str] = None


class ResearchResponse(BaseModel):
    """Response model for competitive research."""
    success: bool
    top_launches: Optional[List[Dict[str, Any]]] = None
    recommended_hunters: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None
    competitor_analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class GitHubRepoInfo(BaseModel):
    """GitHub repository information."""
    owner: str
    repo: str
    description: str
    stars: int
    language: str
    topics: List[str] = []
    readme: Optional[str] = None


class MemorySummaryResponse(BaseModel):
    """Response model for memory summary."""
    success: bool
    user_id: str
    session_id: str
    preferences: List[str] = []
    semantic_memories: List[str] = []
    total_memories: int = 0
    error: Optional[str] = None


class UserSessionResponse(BaseModel):
    """Response model for user session information."""
    success: bool
    user_id: str
    session_id: str
    memory_enabled: bool
    error: Optional[str] = None