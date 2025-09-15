"""FastAPI application for Product Hunt Launch Assistant."""

import sys
import os
import logging
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "src"))

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import json
import asyncio
import time

from api.models import (
    ProductRequest,
    ChatRequest,
    AgentResponse,
    TimelineResponse,
    MarketingAssetsResponse,
    ResearchResponse,
    GitHubRepoInfo,
    MemorySummaryResponse,
    UserSessionResponse
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

# Add custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for {request.url}: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Request validation failed",
            "url": str(request.url)
        }
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize the agent (singleton pattern)
agent = None

def get_agent(user_id: str = None, session_id: str = None):
    """Get or create the Product Hunt agent instance."""
    global agent
    if agent is None:
        try:
            logger.info("Initializing Product Hunt Launch Agent...")
            agent = ProductHuntLaunchAgent()
            logger.info("Agent initialized successfully!")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            logger.error(traceback.format_exc())
            raise e
    if agent is None or (user_id and agent.get_user_id() != user_id):
        agent = ProductHuntLaunchAgent(user_id=user_id, session_id=session_id)
    return agent


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Serve the chat interface."""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Product Hunt Launch Assistant"}


@app.post("/api/chat", response_model=AgentResponse)
async def chat_with_agent(request: ChatRequest):
    """General chat endpoint with the Product Hunt assistant."""
    try:
        logger.info(f"Chat request: {request.message[:100]}...")
        agent_instance = get_agent()
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)
        response = agent_instance.chat(request.message)
        logger.info("Chat response generated successfully")

        # Extract text content from AgentResult if needed
        logger.info(f"Chat response type: {type(response)}")

        if hasattr(response, 'content') and hasattr(response.content, 'text'):
            response_text = response.content.text
        elif hasattr(response, 'content'):
            response_text = str(response.content)
        elif hasattr(response, 'text'):
            response_text = response.text
        elif isinstance(response, str):
            response_text = response
        else:
            # Try to extract from the string representation
            response_str = str(response)
            if 'text=' in response_str:
                import re
                match = re.search(r"text='([^']*)'", response_str)
                if match:
                    response_text = match.group(1)
                else:
                    response_text = response_str
            else:
                response_text = response_str

        return AgentResponse(
            success=True,
            response=response,
            data={
                "context": request.context,
                "user_id": agent_instance.get_user_id(),
                "session_id": agent_instance.get_session_id()
            }
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/api/chat-stream")
async def chat_with_agent_stream(request: ChatRequest):
    """Real streaming chat endpoint with the Product Hunt assistant."""

    # Validate message is a string
    if not isinstance(request.message, str):
        logger.error(f"Invalid message type: {type(request.message)}, value: {request.message}")
        raise HTTPException(status_code=400, detail="Message must be a string")

    if not request.message.strip():
        logger.error("Empty message received")
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Received chat stream request: {request.message[:50]}...")
    logger.info(f"Request context keys: {list(request.context.keys()) if request.context else 'None'}")

    async def generate_response():
        try:
            logger.info(f"Streaming chat request: {request.message[:100]}...")
            agent_instance = get_agent()

            # Send start signal
            yield f"data: {json.dumps({'type': 'start'})}\n\n"

            accumulated_text = ""

            # Get the full response first (Strands may not support true streaming)
            response = agent_instance.chat(request.message)
            logger.info("Chat response generated, starting streaming simulation")

            # Extract text content from AgentResult
            response_text = ""
            if hasattr(response, 'content') and hasattr(response.content, 'text'):
                response_text = response.content.text
            elif hasattr(response, 'content'):
                response_text = str(response.content)
            elif hasattr(response, 'text'):
                response_text = response.text
            elif isinstance(response, str):
                response_text = response
            else:
                response_str = str(response)
                import re
                patterns = [
                    r"text='([^']*)'",
                    r'"text":\s*"([^"]*)"',
                    r'text=([^,\)]*)'
                ]

                for pattern in patterns:
                    match = re.search(pattern, response_str, re.DOTALL)
                    if match:
                        response_text = match.group(1)
                        break

                if not response_text:
                    response_text = response_str

            logger.info(f"Extracted response text length: {len(response_text)}")

            # Stream character by character for more realistic feel
            accumulated_text = ""
            word_buffer = ""

            for i, char in enumerate(response_text):
                accumulated_text += char
                word_buffer += char

                # Send chunks on word boundaries or every few characters
                if char in ' \n\t.,!?;:' or (i > 0 and i % 3 == 0):
                    if word_buffer.strip():  # Only send if there's actual content
                        # Send token data
                        data = {
                            "type": "token",
                            "content": word_buffer,
                            "accumulated": accumulated_text,
                            "done": False
                        }

                        yield f"data: {json.dumps(data)}\n\n"
                        word_buffer = ""

                        # Add delay for realistic streaming feel
                        await asyncio.sleep(0.02)  # 20ms delay

            # Send any remaining buffer
            if word_buffer.strip():
                data = {
                    "type": "token",
                    "content": word_buffer,
                    "accumulated": accumulated_text,
                    "done": False
                }
                yield f"data: {json.dumps(data)}\n\n"

            # Send completion signal
            completion_data = {
                "type": "complete",
                "content": accumulated_text,
                "done": True
            }
            yield f"data: {json.dumps(completion_data)}\n\n"

            logger.info("Streaming response completed")

        except Exception as e:
            logger.error(f"Streaming chat error: {e}")
            logger.error(traceback.format_exc())

            error_data = {
                "type": "error",
                "error": str(e),
                "done": True
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )


@app.post("/api/analyze-product", response_model=AgentResponse)
async def analyze_product(request: ProductRequest):
    """Analyze a product and provide comprehensive launch guidance."""
    try:
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)

        # Seed memory with product information
        product_data = {
            "product_name": request.product_name,
            "product_type": request.product_type,
            "product_description": request.product_description,
            "target_audience": request.target_audience,
            "launch_date": request.launch_date,
            "additional_notes": request.additional_notes,
            "github_repo": request.github_repo
        }
        agent_instance.seed_product_memory(product_data)

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

        logger.info("Sending prompt to agent...")
        response = agent_instance.chat(prompt)
        logger.info("Product analysis completed successfully")

        # Extract text content from AgentResult if needed
        logger.info(f"Analysis response type: {type(response)}")

        if hasattr(response, 'content') and hasattr(response.content, 'text'):
            response_text = response.content.text
        elif hasattr(response, 'content'):
            response_text = str(response.content)
        elif hasattr(response, 'text'):
            response_text = response.text
        elif isinstance(response, str):
            response_text = response
        else:
            # Try to extract from the string representation
            response_str = str(response)
            if 'text=' in response_str:
                import re
                match = re.search(r"text='([^']*)'", response_str)
                if match:
                    response_text = match.group(1)
                else:
                    response_text = response_str
            else:
                response_text = response_str

        return AgentResponse(
            success=True,
            response=response_text,
            data={
                "product_info": request.dict(),
                "analysis_type": "comprehensive",
                "user_id": agent_instance.get_user_id(),
                "session_id": agent_instance.get_session_id()
            }
        )
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/generate-timeline", response_model=TimelineResponse)
async def generate_timeline(request: ProductRequest):
    """Generate a launch timeline for the product."""
    try:
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)

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
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)
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
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)
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


@app.post("/api/memory/summary", response_model=MemorySummaryResponse)
async def get_memory_summary(request: ChatRequest):
    """Get a summary of user's stored memories."""
    try:
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)
        memory_summary = agent_instance.get_memory_summary()
        
        return MemorySummaryResponse(
            success=True,
            user_id=agent_instance.get_user_id(),
            session_id=agent_instance.get_session_id(),
            preferences=memory_summary.get("preferences", []),
            semantic_memories=memory_summary.get("semantic", []),
            total_memories=memory_summary.get("total_memories", 0)
        )
    except Exception as e:
        return MemorySummaryResponse(
            success=False,
            user_id=request.user_id or "unknown",
            session_id=request.session_id or "unknown",
            error=f"Memory summary error: {str(e)}"
        )


@app.post("/api/memory/seed", response_model=AgentResponse)
async def seed_memory(request: ProductRequest):
    """Seed memory with product information."""
    try:
        agent_instance = get_agent(user_id=request.user_id, session_id=request.session_id)
        
        product_data = {
            "product_name": request.product_name,
            "product_type": request.product_type,
            "product_description": request.product_description,
            "target_audience": request.target_audience,
            "launch_date": request.launch_date,
            "additional_notes": request.additional_notes,
            "github_repo": request.github_repo
        }
        
        success = agent_instance.seed_product_memory(product_data)
        
        if success:
            return AgentResponse(
                success=True,
                response="Product information successfully seeded to memory",
                data={
                    "user_id": agent_instance.get_user_id(),
                    "session_id": agent_instance.get_session_id(),
                    "product_info": product_data
                }
            )
        else:
            return AgentResponse(
                success=False,
                response="Failed to seed product memory",
                error="Memory seeding failed"
            )
    except Exception as e:
        return AgentResponse(
            success=False,
            response="Error seeding memory",
            error=f"Memory seeding error: {str(e)}"
        )


@app.post("/api/session/create", response_model=UserSessionResponse)
async def create_user_session():
    """Create a new user session with memory enabled."""
    try:
        agent_instance = get_agent()
        
        return UserSessionResponse(
            success=True,
            user_id=agent_instance.get_user_id(),
            session_id=agent_instance.get_session_id(),
            memory_enabled=agent_instance.memory_hooks is not None
        )
    except Exception as e:
        return UserSessionResponse(
            success=False,
            user_id="unknown",
            session_id="unknown",
            memory_enabled=False,
            error=f"Session creation error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)