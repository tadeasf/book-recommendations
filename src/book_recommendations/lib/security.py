from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import API_KEY

API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Validate the API key from the X-API-Key header.
    
    Args:
        api_key_header: The API key from the request header
        
    Returns:
        str: The validated API key
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API key"
    )