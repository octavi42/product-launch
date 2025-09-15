# Bedrock Model Setup Guide

## 🚀 Model Configuration

Your Product Hunt Launch Assistant is now configured to use:

- **Model ID**: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
- **Region**: `us-west-2` (default)
- **Temperature**: `0.3` (balanced creativity/consistency)

## 🔧 AWS Setup

### 1. Set AWS Credentials

```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_REGION=us-west-2
```

### 2. Verify Model Access

```bash
# Test the model connection
make test-model
# or
python test_model.py
```

### 3. Check Available Models

If you get model errors, check what models are available in your AWS account:

1. Go to AWS Bedrock Console
2. Navigate to "Foundation models"
3. Look for Claude models in your region
4. Update the model ID in `app/utils.py` if needed

## 🧪 Testing

```bash
# Test application import
make test

# Test model connection
make test-model

# Run the full application
make run
```

## 🔄 Model Configuration

To change the model, edit `app/utils.py`:

```python
class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )
        self.model_id = "your-model-id-here"
        self.temperature = 0.3  # Adjust creativity (0.0-1.0)
```

## 🚨 Troubleshooting

### Common Issues

1. **ValidationException**: Model not available in your region

   - Check AWS Bedrock console for available models
   - Update model ID or region

2. **AccessDeniedException**: Missing permissions

   - Ensure your AWS credentials have Bedrock access
   - Check IAM permissions

3. **Region Issues**: Model not available in region
   - Try different regions (us-east-1, us-west-2, etc.)
   - Update AWS_REGION environment variable

### Quick Fixes

```bash
# Check current region
echo $AWS_REGION

# Test with different region
export AWS_REGION=us-east-1
make test-model

# Reset to default
export AWS_REGION=us-west-2
```

## ✅ Success Indicators

When everything is working, you should see:

```
✅ Bedrock client initialized
   Model ID: us.anthropic.claude-3-7-sonnet-20250219-v1:0
   Temperature: 0.3
   Region: us-west-2

✅ Model response received:
   Model is working!
```

Your Product Hunt Launch Assistant is ready! 🎉
