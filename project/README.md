# AWS Bedrock Customer Support Agent

A customer support agent built on AWS Bedrock using the Strands Agents framework and Claude 3.7 Sonnet.

## Features

- **Product Information**: Get detailed specs and information about electronics
- **Return Policy Lookup**: Access return policies for different product categories
- **Web Search**: Search the web for up-to-date troubleshooting information
- **Interactive Chat**: Command-line interface for testing and interaction

## Prerequisites

- AWS account with Bedrock access
- Python 3.10+
- AWS CLI configured with proper credentials
- Anthropic Claude 3.7 Sonnet enabled in Amazon Bedrock

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
- Confirm Claude 3.7 Sonnet availability

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Your AWS credentials are already configured in `.env`

### Quick Start

Run the agent using the convenient script:
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
from src.agent import CustomerSupportAgent

agent = CustomerSupportAgent()
response = agent.chat("What's the return policy for smartphones?")
print(response)
```

## Project Structure

```
project/
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
├── src/
│   ├── agent.py           # Main agent implementation
│   ├── tools/             # Tool implementations
│   │   ├── __init__.py
│   │   └── product_tools.py
│   └── helpers/           # Utility functions
│       ├── __init__.py
│       └── utils.py
└── README.md
```

## Available Tools

1. **get_return_policy(product_category)** - Returns policy information for product categories
2. **get_product_info(product_type)** - Provides technical specifications and details
3. **web_search(keywords)** - Searches the web for current information

## Example Queries

- "What's the return policy for my laptop?"
- "Tell me about smartphone features"
- "My phone won't charge, what should I do?"
- "What are the specs for gaming monitors?"

## Next Steps

This is a basic implementation. The bedrock-agentcore-workshop shows how to enhance it with:

- **Lab 2**: Persistent memory across conversations
- **Lab 3**: Shared tools via AgentCore Gateway
- **Lab 4**: Production deployment with AgentCore Runtime
- **Lab 5**: Web interface with authentication

## Architecture

Currently running as a local prototype. Future labs will migrate to:
- AgentCore Memory for conversation persistence
- AgentCore Gateway for shared tool management
- AgentCore Runtime for production deployment
- AgentCore Identity for authentication and authorization