# Agentcore Memory Integration

This document describes the Agentcore Memory integration added to the Product Hunt Launch Assistant.

## Overview

The Product Hunt Launch Assistant now includes persistent memory capabilities using Amazon Bedrock Agentcore Memory. This allows the assistant to:

- **Remember product context** across conversations
- **Learn user preferences** and communication style
- **Maintain launch progress** and recommendations
- **Provide personalized advice** based on previous interactions

## Architecture

### Memory Strategies

The system uses two memory strategies:

1. **USER_PREFERENCE**: Stores user preferences, communication style, and behavioral patterns
   - Namespace: `producthunt/user/{actorId}/preferences`
   - Examples: Preferred launch timing, communication tone, strategic approach

2. **SEMANTIC**: Stores factual information about products and launch strategies
   - Namespace: `producthunt/user/{actorId}/semantic`
   - Examples: Product details, launch timeline, marketing assets, competitive insights

### Components

#### 1. Memory Helper Module (`src/helpers/memory.py`)
- `create_or_get_memory_resource()`: Creates or retrieves Agentcore Memory resource
- `ProductHuntMemoryHooks`: Strands hooks for automatic memory operations
- `seed_product_memory()`: Seeds memory with initial product information
- `get_user_memory_summary()`: Retrieves memory summary for display

#### 2. Enhanced Agent (`src/agent.py`)
- Memory hooks integration
- User and session management
- Memory seeding and retrieval methods

#### 3. API Enhancements (`api/main.py`)
- User identification in all endpoints
- Memory management endpoints
- Session creation and management

#### 4. Frontend Updates (`templates/index.html`, `static/app.js`)
- User session initialization
- Memory status display
- Context visualization

## Features

### Automatic Memory Operations

The system automatically:

1. **Retrieves context** before processing each user query
2. **Saves interactions** after each agent response
3. **Seeds product information** when analyzing products
4. **Maintains user sessions** across requests

### Memory Management

- **User Identification**: Each user gets a unique ID for memory isolation
- **Session Management**: Sessions track conversation context
- **Memory Expiry**: Memories expire after 90 days
- **Namespace Isolation**: User data is isolated by namespace

### API Endpoints

#### New Memory Endpoints

- `POST /api/memory/summary`: Get user's memory summary
- `POST /api/memory/seed`: Seed memory with product information
- `POST /api/session/create`: Create new user session

#### Enhanced Existing Endpoints

All existing endpoints now support:
- `user_id`: User identification
- `session_id`: Session tracking
- Automatic memory context injection

## Usage

### Frontend Usage

The frontend automatically:
1. Creates a user session on page load
2. Seeds memory when analyzing products
3. Displays memory status and context
4. Maintains user identification across requests

### API Usage

```python
# Create agent with memory
agent = ProductHuntLaunchAgent(user_id="user123", session_id="session456")

# Seed product memory
product_data = {
    "product_name": "MyApp",
    "product_type": "SaaS",
    "product_description": "A great app",
    "target_audience": "developers"
}
agent.seed_product_memory(product_data)

# Chat with memory context
response = agent.chat("What do you know about my product?")
```

### Memory Context Display

The frontend shows:
- Memory enabled status
- Number of stored memories
- Recent preferences and product details
- Context used in recommendations

## Configuration

### Environment Variables

Ensure these are set in your `.env` file:
```
AWS_DEFAULT_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### AWS Permissions

The system requires these AWS permissions:
- `bedrock:CreateMemory`
- `bedrock:GetMemory`
- `bedrock:RetrieveMemories`
- `bedrock:CreateEvent`
- `bedrock:DeleteMemory`
- `ssm:PutParameter`
- `ssm:GetParameter`

## Testing

Run the memory integration test:

```bash
cd project
python test_memory.py
```

This will test:
- Memory resource creation
- Product memory seeding
- Memory retrieval
- Conversation with context

## Benefits

### For Users
- **Personalized Experience**: Recommendations based on their specific product and preferences
- **Context Continuity**: No need to re-explain product details
- **Progress Tracking**: Assistant remembers launch timeline and progress
- **Consistent Advice**: Recommendations build on previous conversations

### For Developers
- **Scalable Architecture**: Multi-user support with isolated memory
- **Automatic Operations**: Memory works transparently
- **Rich Context**: Access to user preferences and product history
- **Easy Integration**: Simple API for memory operations

## Troubleshooting

### Common Issues

1. **Memory not created**: Check AWS credentials and permissions
2. **Context not retrieved**: Verify user_id and session_id are consistent
3. **Memory not persisting**: Check if memory hooks are properly registered

### Debug Mode

Enable debug logging to see memory operations:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Future Enhancements

- **Memory Analytics**: Track memory usage and effectiveness
- **Memory Management UI**: Allow users to view and edit their memories
- **Cross-Product Memory**: Share context across multiple products
- **Memory Export**: Export user memories for backup or migration
