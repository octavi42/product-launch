from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.coordinator import AgentCoordinator
from app.models import AgentResponse, AssetPrepRequest, PlanningRequest, ResearchRequest

# Initialize FastAPI app
app = FastAPI(
    title="Product Hunt Launch Assistant",
    description="AI-powered agents for Product Hunt launch planning",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinator
coordinator = AgentCoordinator()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="""
        <html>
            <head><title>Product Hunt Launch Assistant</title></head>
            <body>
                <h1>Product Hunt Launch Assistant</h1>
                <p>API is running! <p>
                <p>Use the endpoints to interact with the agents.</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """
        )


@app.get("/agents")
async def get_agents():
    """Get available agents"""
    return coordinator.get_available_agents()


@app.post("/agents/planning", response_model=AgentResponse)
async def planning_agent(request: PlanningRequest):
    """Generate launch timeline and checklist"""
    request_data = request.dict()
    return coordinator.route_request("planning", request_data)


@app.post("/agents/asset-prep", response_model=AgentResponse)
async def asset_prep_agent(request: AssetPrepRequest):
    """Generate marketing assets"""
    request_data = request.dict()
    return coordinator.route_request("asset_prep", request_data)


@app.post("/agents/research", response_model=AgentResponse)
async def research_agent(request: ResearchRequest):
    """Research top launches and find hunters"""
    request_data = request.dict()
    return coordinator.route_request("research", request_data)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Product Launch is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
