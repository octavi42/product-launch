.PHONY: format lint test run clean install

# Install dependencies
install:
	pip install -r requirements.txt

# Format code automatically
format:
	python fix_code.py

# Run linting
lint:
	flake8 app/ --max-line-length 88 --extend-ignore E203,W503,E501

# Run the application
run:
	python run.py

# Test the application
test:
	python -c "from app.main import app; print('✅ App imports successfully')"

# Test the Bedrock model
test-model:
	python test_model.py

# Test Strands agents
test-strands:
	python test_strands_simple.py

# Test model fix
test-model-fix:
	python test_model_fix.py

# Test response format fix
test-response-fix:
	python test_response_fix.py

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Quick setup for hackathon
setup: install format test
	@echo "🚀 Product Hunt Launch Assistant is ready!"
	@echo "Run 'make test-response-fix' to test the API response format"
	@echo "Run 'make test-model-fix' to test the corrected model"
	@echo "Run 'make test-strands' to test Strands agents"
	@echo "Run 'make run' to start the application"
