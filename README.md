# Product Hunt Launch Assistant

AI-powered agents to help founders launch successfully on Product Hunt. Built with AWS Bedrock and FastAPI for a 4-hour hackathon.

## 🚀 Features

### 3 Specialized AI Agents

1. **Planning Agent** 📅
   - Generate comprehensive launch timelines
   - Create actionable checklists with deadlines
   - Smart date parsing ("next Tuesday", "December 15")
   - Industry-specific considerations

2. **Asset Prep Agent** ✍️
   - Generate compelling taglines (5 options)
   - Create Product Hunt descriptions
   - Generate social media tweets
   - A/B testing suggestions

3. **Research Agent** 🔍
   - Research top Product Hunt launches
   - Find relevant hunters for your domain
   - Competitive analysis and insights
   - Market positioning recommendations

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **AI**: AWS Bedrock (Claude 3.5 Sonnet)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Ready for AWS/Heroku

## 🚀 Quick Start

### Prerequisites

1. AWS Account with Bedrock access
2. Python 3.8+
3. AWS credentials configured

### Installation

```bash
# Clone and setup
git clone <your-repo>
cd productlaunch

# Install dependencies
pip install -r requirements.txt

# Set AWS credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1

# Run the application
python -m app.main
```

### Access the App

- **Web Interface**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Planning Agent
```bash
POST /agents/planning
{
  "product_name": "MyAwesomeApp",
  "product_type": "SaaS",
  "launch_date": "next Tuesday",
  "additional_notes": "Focus on developer tools"
}
```

### Asset Prep Agent
```bash
POST /agents/asset-prep
{
  "product_name": "MyAwesomeApp",
  "elevator_pitch": "AI-powered writing assistant for developers",
  "target_audience": "Software developers",
  "tone": "professional"
}
```

### Research Agent
```bash
POST /agents/research
{
  "product_category": "Developer Tools",
  "target_audience": "Software developers",
  "budget_range": "Under $500"
}
```

## 🎯 Hackathon Demo

### Demo Scenario
"Launch my AI writing tool next Friday"

1. **Planning Agent**: Shows 15-day timeline with specific tasks
2. **Asset Prep Agent**: Generates 5 taglines, description, 3 tweets
3. **Research Agent**: Finds top AI tool launches and relevant hunters

### Key Features for Demo
- ✅ Single-click agent selection
- ✅ Real-time AI responses
- ✅ Export-ready content
- ✅ Mobile-responsive design
- ✅ Error handling

## 🏗️ Architecture

```
app/
├── main.py              # FastAPI application
├── coordinator.py       # Agent router
├── models.py           # Pydantic data models
├── utils.py            # Shared utilities
└── agents/
    ├── base_agent.py   # Base agent class
    ├── planning_agent.py
    ├── asset_prep_agent.py
    └── research_agent.py
```

## 🔧 Configuration

### Environment Variables
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

### AWS Bedrock Setup
1. Enable Claude 3.5 Sonnet in AWS Bedrock
2. Configure IAM permissions for Bedrock access
3. Set up proper region (us-east-1 recommended)

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (Heroku)
```bash
# Add Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

## 📊 Performance

- **Response Time**: 2-5 seconds per agent
- **Concurrent Users**: 100+ (FastAPI async)
- **Cost**: ~$0.01 per request (Bedrock pricing)

## 🎪 Demo Tips

1. **Pre-load sample data** for quick demos
2. **Show all 3 agents** in sequence
3. **Highlight time savings** vs manual research
4. **Export final plan** as document
5. **Mobile demo** to show responsiveness

## 🔮 Future Enhancements

- [ ] Hunter outreach automation
- [ ] Social media scheduling
- [ ] Launch performance tracking
- [ ] Integration with Product Hunt API
- [ ] Team collaboration features

## 📝 License

MIT License - Built for hackathon demonstration

---

**Built in 4 hours for Product Hunt Launch Assistant Hackathon** 🚀
