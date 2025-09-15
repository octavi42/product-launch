"""
Product Hunt Launch Assistant Tools using Strands Agents
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from dateutil import parser

from strands import tool


@tool
def generate_launch_timeline(
    product_name: str,
    product_type: str,
    launch_date: str,
    additional_notes: str = ""
) -> Dict[str, Any]:
    """
    Generate a comprehensive launch timeline and checklist for Product Hunt launch.
    
    Args:
        product_name: Name of the product to launch
        product_type: Type of product (SaaS, Mobile App, Chrome Extension, etc.)
        launch_date: Target launch date (e.g., "next Tuesday", "December 15, 2024")
        additional_notes: Any additional requirements or constraints
        
    Returns:
        Dictionary containing timeline, milestones, and key tasks
    """
    try:
        # Parse launch date
        parsed_date = parse_launch_date(launch_date)
        days_until_launch = calculate_timeline_days(parsed_date)
        
        if days_until_launch < 0:
            return {
                "success": False,
                "error": "Launch date is in the past. Please provide a future date."
            }
        
        # Generate timeline based on days until launch
        timeline = create_timeline(product_name, product_type, parsed_date, days_until_launch, additional_notes)
        milestones = extract_milestones(timeline)
        
        return {
            "success": True,
            "timeline": timeline,
            "total_days": days_until_launch,
            "launch_date": format_date_for_display(parsed_date),
            "key_milestones": milestones
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Timeline generation failed: {str(e)}"
        }


@tool
def generate_marketing_assets(
    product_name: str,
    elevator_pitch: str,
    target_audience: str,
    tone: str = "professional"
) -> Dict[str, Any]:
    """
    Generate marketing assets including taglines, descriptions, and social media content.
    
    Args:
        product_name: Name of the product
        elevator_pitch: Brief description of the product's value proposition
        target_audience: Primary target audience
        tone: Tone for the content (professional, casual, playful, technical)
        
    Returns:
        Dictionary containing taglines, description, tweets, and suggestions
    """
    try:
        # Generate taglines
        taglines = [
            f"{product_name} - {elevator_pitch[:50]}...",
            f"Revolutionary {product_name} for {target_audience}",
            f"Transform your workflow with {product_name}",
            f"The future of {product_name} is here",
            f"Build better with {product_name}"
        ]
        
        # Generate short description
        short_description = f"{elevator_pitch} Perfect for {target_audience}. Try {product_name} today and see the difference!"
        
        # Generate tweets
        tweets = [
            f"🚀 Just launched {product_name} on @ProductHunt! {elevator_pitch[:100]}... #ProductHunt #Launch",
            f"Excited to share {product_name} with the world! Built for {target_audience}. Check it out: #ProductHunt #Launch",
            f"After months of building, {product_name} is live on @ProductHunt! Would love your support 🙏 #ProductHunt #Launch"
        ]
        
        # Generate suggestions
        suggestions = [
            f"Start building your community around {product_name} 2-3 weeks before launch",
            f"Create a demo video showcasing {product_name}'s key features",
            f"Reach out to {target_audience} influencers and thought leaders",
            "Prepare social media content for launch day and the following week",
            "Plan follow-up activities to maintain momentum after launch day"
        ]
        
        return {
            "success": True,
            "taglines": taglines,
            "short_description": short_description,
            "tweets": tweets,
            "suggestions": suggestions
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Asset generation failed: {str(e)}"
        }


@tool
def research_top_launches(
    product_category: str,
    target_audience: str,
    budget_range: str = ""
) -> Dict[str, Any]:
    """
    Research top Product Hunt launches and find relevant hunters for your domain.
    
    Args:
        product_category: Category of the product (e.g., Productivity, AI Tools, Design)
        target_audience: Primary target audience
        budget_range: Budget range for hunter outreach (optional)
        
    Returns:
        Dictionary containing top launches, recommended hunters, and insights
    """
    try:
        # Mock data for demo - in real implementation, this would use web search
        top_launches = [
            {
                "name": f"Top {product_category} Tool",
                "tagline": "Revolutionary solution for modern teams",
                "launch_date": "2024-10-15",
                "ranking": "1st place",
                "success_factors": ["Strong community", "Clear value prop", "Great timing"],
                "standout_features": "Unique approach to common problem",
                "lessons": "Focus on user experience and community building"
            },
            {
                "name": f"AI-Powered {product_category}",
                "tagline": "Automate your workflow with AI",
                "launch_date": "2024-09-20",
                "ranking": "2nd place",
                "success_factors": ["AI trend", "Clear demo", "Founder story"],
                "standout_features": "First to market with AI integration",
                "lessons": "Timing and trend alignment crucial"
            }
        ]
        
        recommended_hunters = [
            {
                "name": "Tech Hunter",
                "handle": "@techhunter",
                "specialization": f"{product_category} and productivity tools",
                "followers": "15K+",
                "success_rate": "High",
                "contact_approach": "Twitter DM or email",
                "why_fit": f"Specializes in {product_category} launches"
            },
            {
                "name": "Startup Advocate",
                "handle": "@startupadvocate",
                "specialization": "Early-stage products",
                "followers": "8K+",
                "success_rate": "Medium-High",
                "contact_approach": "LinkedIn message",
                "why_fit": "Great at helping new founders"
            }
        ]
        
        insights = [
            f"Products in {product_category} that launch on Tuesdays perform 20% better",
            "Community building 2-3 weeks before launch is crucial for success",
            "Clear, benefit-focused taglines outperform feature-focused ones",
            "Founder stories and behind-the-scenes content drive engagement",
            "Posting updates and responding to comments increases visibility"
        ]
        
        competitor_analysis = {
            "market_saturation": "Medium",
            "pricing_strategies": ["Freemium", "One-time purchase", "Subscription"],
            "key_differentiators": ["User experience", "AI integration", "Community features"],
            "market_gaps": ["Better onboarding", "Mobile-first approach", "Enterprise features"],
            "positioning_strategy": "Focus on unique value proposition and user experience"
        }
        
        return {
            "success": True,
            "top_launches": top_launches,
            "recommended_hunters": recommended_hunters,
            "insights": insights,
            "competitor_analysis": competitor_analysis
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Research failed: {str(e)}"
        }


# Helper functions
def parse_launch_date(date_input: str) -> datetime:
    """Parse natural language date input"""
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


def create_timeline(product_name: str, product_type: str, launch_date: datetime, days_until_launch: int, additional_notes: str) -> List[Dict[str, Any]]:
    """Create detailed timeline based on days until launch"""
    timeline = []
    
    if days_until_launch >= 14:
        timeline.append({
            "phase": "Pre-launch (2+ weeks before)",
            "tasks": [
                {
                    "name": "Create Product Hunt account and profile",
                    "due_date": f"{days_until_launch - 14} days before launch",
                    "priority": "High",
                    "time_estimate": "1 hour",
                    "dependencies": "None",
                    "success_criteria": "Account created with complete profile"
                },
                {
                    "name": "Prepare product assets (logo, screenshots, demo video)",
                    "due_date": f"{days_until_launch - 10} days before launch",
                    "priority": "High",
                    "time_estimate": "4-6 hours",
                    "dependencies": "None",
                    "success_criteria": "All visual assets ready"
                }
            ]
        })
    
    if days_until_launch >= 7:
        timeline.append({
            "phase": "Final preparation (1 week before)",
            "tasks": [
                {
                    "name": "Write compelling product description and tagline",
                    "due_date": f"{days_until_launch - 7} days before launch",
                    "priority": "High",
                    "time_estimate": "2-3 hours",
                    "dependencies": "Product assets ready",
                    "success_criteria": "Description approved and ready"
                },
                {
                    "name": "Identify and reach out to potential hunters",
                    "due_date": f"{days_until_launch - 5} days before launch",
                    "priority": "High",
                    "time_estimate": "3-4 hours",
                    "dependencies": "None",
                    "success_criteria": "At least 3 hunters confirmed"
                }
            ]
        })
    
    timeline.append({
        "phase": "Launch day",
        "tasks": [
            {
                "name": "Submit product to Product Hunt",
                "due_date": "Launch day (12:01 AM PST)",
                "priority": "High",
                "time_estimate": "30 minutes",
                "dependencies": "All assets and hunters ready",
                "success_criteria": "Product live on Product Hunt"
            },
            {
                "name": "Share on social media and personal networks",
                "due_date": "Launch day (morning)",
                "priority": "High",
                "time_estimate": "2-3 hours",
                "dependencies": "Product live",
                "success_criteria": "Initial momentum generated"
            }
        ]
    })
    
    return timeline


def extract_milestones(timeline: List[Dict[str, Any]]) -> List[str]:
    """Extract key milestones from timeline"""
    milestones = []
    for phase in timeline:
        for task in phase.get('tasks', []):
            if task.get('priority') == 'High':
                milestones.append(f"{task['name']} - {task['due_date']}")
    return milestones[:5]  # Top 5 milestones
