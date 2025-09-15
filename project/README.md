# Product Hunt Launch Assistant

An AI-powered Product Hunt launch assistant built on AWS Bedrock using the Strands Agents framework and Claude 3.5 Haiku.

## Features

- **Launch Timeline Generation**: Create comprehensive launch plans with tasks, deadlines, and milestones
- **Marketing Asset Creation**: Generate taglines, descriptions, tweets, and promotional content
- **Competitive Research**: Analyze successful launches and identify strategic opportunities
- **Hunter Recommendations**: Find and connect with relevant Product Hunt hunters
- **Strategic Guidance**: Get tactical advice based on proven Product Hunt success patterns
- **Interactive Chat**: Command-line interface for launch planning and optimization

## Prerequisites

- AWS account with Bedrock access
- Python 3.10+
- AWS CLI configured with proper credentials
- Anthropic Claude 3.5 Haiku enabled in Amazon Bedrock

## Installation

### Option 1: Automatic Setup (Recommended)

1. Run the setup script:
```bash
python setup.py
```

This will:
- Install all dependencies
- Test your AWS credentials
- Verify Bedrock access
- Confirm Claude 3.5 Haiku availability

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Your AWS credentials are already configured in `.env`

## Usage Options

### 🌐 Web Interface (Recommended)

Run the web application:
```bash
python run_web.py
```

Then open your browser to:
- **Web App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Reference**: http://localhost:8000/redoc

### 💬 Command Line

Run the agent in CLI mode:
```bash
./run.sh
```

Or run directly:
```bash
python main.py
```

## Usage

### Interactive Mode

Run the agent in interactive chat mode:

```bash
python main.py
```

### Programmatic Usage

```python
from src.agent import ProductHuntLaunchAgent

agent = ProductHuntLaunchAgent()
response = agent.chat("Help me create a launch timeline for my SaaS product launching next Tuesday")
print(response)
```

## Project Structure

```
project/
├── main.py                 # CLI entry point
├── run_web.py             # Web app entry point
├── requirements.txt        # Dependencies
├── api/                   # FastAPI backend
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   └── models.py         # Pydantic models
├── src/                   # Core agent code
│   ├── agent.py          # Product Hunt launch assistant
│   ├── tools/            # Tool implementations
│   │   ├── __init__.py
│   │   └── product_tools.py  # Product Hunt launch tools
│   └── helpers/          # Utility functions
│       ├── __init__.py
│       └── utils.py
├── templates/             # HTML templates
│   └── index.html        # Main web interface
├── static/               # Static assets
│   └── app.js           # Frontend JavaScript
└── README.md
```

## Available Tools

1. **generate_launch_timeline(product_name, product_type, launch_date, additional_notes)** - Creates comprehensive launch timelines with tasks, deadlines, and milestones
2. **generate_marketing_assets(product_name, elevator_pitch, target_audience, tone)** - Generates taglines, descriptions, tweets, and promotional content
3. **research_top_launches(product_category, target_audience, budget_range)** - Analyzes successful launches and provides competitive insights

## Example Queries

- "Help me create a launch timeline for my SaaS product launching next Tuesday"
- "Generate marketing assets for my productivity app targeting remote workers"
- "Research successful AI tool launches and find relevant hunters"
- "What's the best day to launch and how should I prepare?"
- "Create compelling taglines for my design tool"

## Product Hunt Success Tips

The assistant incorporates proven Product Hunt strategies:

- **Optimal Launch Days**: Tuesday-Thursday typically perform best
- **Community Building**: Start building relationships 2-3 weeks before launch
- **Clear Messaging**: Benefit-focused taglines outperform feature lists
- **Authentic Stories**: Founder narratives and behind-the-scenes content drive engagement
- **Launch Day Engagement**: Consistent updates and responses maximize visibility

## Enhancement Opportunities

Based on the bedrock-agentcore-workshop, this can be enhanced with:

- **Lab 2**: Persistent memory to track launch progress across sessions
- **Lab 3**: Shared tools via AgentCore Gateway for team collaboration
- **Lab 4**: Production deployment with AgentCore Runtime and observability
- **Lab 5**: Web interface for easier access and team sharing

## Architecture

Currently running as a local prototype with specialized Product Hunt tools. Future enhancements could include:
- AgentCore Memory for launch campaign tracking
- AgentCore Gateway for team tool sharing
- AgentCore Runtime for production deployment
- Integration with Product Hunt API for real-time data