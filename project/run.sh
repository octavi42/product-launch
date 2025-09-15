#!/bin/bash

# AWS Bedrock Customer Support Agent Runner

echo "🤖 AWS Bedrock Customer Support Agent"
echo "===================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and add your credentials"
    exit 1
fi

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

echo "✅ AWS credentials loaded from .env"
echo "Region: $AWS_DEFAULT_REGION"

# Run the agent
python main.py