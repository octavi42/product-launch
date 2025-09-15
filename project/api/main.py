"""FastAPI application for Product Hunt Launch Assistant."""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from api.models import (
    ProductRequest,
    ChatRequest,
    AgentResponse,
    TimelineResponse,
    MarketingAssetsResponse,
    ResearchResponse,
    GitHubRepoInfo
)
from src.agent import ProductHuntLaunchAgent

# Initialize FastAPI app
app = FastAPI(
    title="Product Hunt Launch Assistant API",
    description="AI-powered assistant for successful Product Hunt launches",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize the agent (singleton pattern)
agent = None

def get_agent():
    """Get or create the Product Hunt agent instance."""
    global agent
    if agent is None:
        agent = ProductHuntLaunchAgent()
    return agent


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Product Hunt Launch Assistant"}


@app.post("/api/chat", response_model=AgentResponse)
async def chat_with_agent(request: ChatRequest):
    """General chat endpoint with the Product Hunt assistant."""
    try:
        agent_instance = get_agent()
        response = agent_instance.chat(request.message)

        return AgentResponse(
            success=True,
            response=response,
            data={"context": request.context} if request.context else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/api/analyze-product", response_model=AgentResponse)
async def analyze_product(request: ProductRequest):
    """Analyze a product and provide comprehensive launch guidance."""
    try:
        agent_instance = get_agent()

        # Create a comprehensive prompt for the agent
        prompt = f"""I need help launching my product on Product Hunt. Here are the details:

Product Name: {request.product_name}
Product Type: {request.product_type}
Description: {request.product_description}
Target Audience: {request.target_audience or 'Not specified'}
Planned Launch Date: {request.launch_date or 'Not specified'}
Additional Notes: {request.additional_notes or 'None'}
GitHub Repository: {request.github_repo or 'Not provided'}

Please provide a comprehensive analysis and recommendations including:
1. Launch timeline and key milestones
2. Marketing strategy and messaging
3. Competitive landscape insights
4. Hunter recommendations
5. Strategic advice for success

Focus on actionable, specific recommendations tailored to my product."""

        response = agent_instance.chat(prompt)

        return AgentResponse(
            success=True,
            response=response,
            data={
                "product_info": request.dict(),
                "analysis_type": "comprehensive"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/generate-timeline", response_model=TimelineResponse)
async def generate_timeline(request: ProductRequest):
    """Generate a launch timeline for the product."""
    try:
        agent_instance = get_agent()

        # Use the timeline tool directly
        from src.tools.product_tools import generate_launch_timeline

        result = generate_launch_timeline(
            product_name=request.product_name,
            product_type=request.product_type,
            launch_date=request.launch_date or "next Tuesday",
            additional_notes=f"Description: {request.product_description}. Target: {request.target_audience}. {request.additional_notes}"
        )

        if result.get("success"):
            return TimelineResponse(
                success=True,
                timeline=result.get("timeline"),
                total_days=result.get("total_days"),
                launch_date=result.get("launch_date"),
                key_milestones=result.get("key_milestones")
            )
        else:
            return TimelineResponse(success=False, error=result.get("error"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Timeline generation error: {str(e)}")


@app.post("/api/generate-marketing", response_model=MarketingAssetsResponse)
async def generate_marketing_assets(request: ProductRequest):
    """Generate marketing assets for the product."""
    try:
        from src.tools.product_tools import generate_marketing_assets

        result = generate_marketing_assets(
            product_name=request.product_name,
            elevator_pitch=request.product_description,
            target_audience=request.target_audience or "entrepreneurs and startups",
            tone="professional"
        )

        if result.get("success"):
            return MarketingAssetsResponse(
                success=True,
                taglines=result.get("taglines"),
                short_description=result.get("short_description"),
                tweets=result.get("tweets"),
                suggestions=result.get("suggestions")
            )
        else:
            return MarketingAssetsResponse(success=False, error=result.get("error"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Marketing assets error: {str(e)}")


@app.post("/api/research-competition", response_model=ResearchResponse)
async def research_competition(request: ProductRequest):
    """Research competitive landscape and successful launches."""
    try:
        from src.tools.product_tools import research_top_launches

        result = research_top_launches(
            product_category=request.product_type,
            target_audience=request.target_audience or "general",
            budget_range="medium"
        )

        if result.get("success"):
            return ResearchResponse(
                success=True,
                top_launches=result.get("top_launches"),
                recommended_hunters=result.get("recommended_hunters"),
                insights=result.get("insights"),
                competitor_analysis=result.get("competitor_analysis")
            )
        else:
            return ResearchResponse(success=False, error=result.get("error"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research error: {str(e)}")


@app.post("/api/connect-github")
async def connect_github_repo(github_url: str):
    """Mock GitHub connection endpoint - will be implemented later."""
    # For now, this is a mock endpoint
    return {
        "success": True,
        "message": "GitHub connection will be implemented in the next phase",
        "repo_info": {
            "url": github_url,
            "status": "mock_connected",
            "note": "This is a placeholder. Real GitHub integration coming soon!"
        }
    }


@app.get("/api/github-info/{owner}/{repo}", response_model=GitHubRepoInfo)
async def get_github_repo_info(owner: str, repo: str):
    """Mock GitHub repository information - will be implemented later."""
    # Mock data for now
    return GitHubRepoInfo(
        owner=owner,
        repo=repo,
        description=f"This is a mock description for {owner}/{repo}",
        stars=42,
        language="Python",
        topics=["ai", "product-hunt", "startup"],
        readme="# Mock README\n\nThis will be populated with real data soon!"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)