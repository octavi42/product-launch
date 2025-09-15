"""Utility functions for AWS Bedrock agent."""

import os
import boto3
from boto3.session import Session
from dotenv import load_dotenv


def load_aws_config():
    """Load AWS configuration from .env file."""
    load_dotenv()

    # Set environment variables if they exist in .env
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_session_token = os.getenv('AWS_SESSION_TOKEN')

    # Set environment variables for boto3
    if aws_access_key:
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
    if aws_secret_key:
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
    if aws_session_token:
        os.environ['AWS_SESSION_TOKEN'] = aws_session_token
    if aws_region:
        os.environ['AWS_DEFAULT_REGION'] = aws_region

    return aws_region


def put_ssm_parameter(name: str, value: str, description: str = ""):
    """Store parameter in AWS Systems Manager Parameter Store."""
    ssm = boto3.client('ssm')
    ssm.put_parameter(
        Name=name,
        Value=value,
        Description=description,
        Type='String',
        Overwrite=True
    )


def get_boto_session():
    """Get boto3 session with current AWS configuration."""
    load_aws_config()
    return Session()


def get_account_region():
    """Get current AWS account ID and region."""
    region = load_aws_config()
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    return account_id, region