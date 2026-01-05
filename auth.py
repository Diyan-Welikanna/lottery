"""
Optional JWT Authentication middleware for the API
Set API_KEY environment variable to enable authentication
"""

from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
import os

# API Key authentication (simple and effective)
API_KEY = os.getenv("API_KEY")  # Set this in Render.com environment variables
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Validate API key from request header.
    If API_KEY env var is not set, authentication is disabled (open API).
    """
    # If no API_KEY is configured, allow all requests (development mode)
    if not API_KEY:
        return None
    
    # If API_KEY is configured, validate it
    if api_key == API_KEY:
        return api_key
    
    raise HTTPException(
        status_code=403,
        detail="Invalid or missing API Key. Add 'X-API-Key' header with your API key."
    )
