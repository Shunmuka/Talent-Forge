"""Authentication dependencies (stub for MVP)."""
from fastapi import HTTPException, Depends
from typing import Optional

# TODO: Implement Google OAuth
# For MVP, we'll use a simple stub that allows all requests
# In production, this should verify JWT tokens from Google OAuth


async def get_current_user(token: Optional[str] = None) -> dict:
    """
    Get current user from authentication token.
    
    For MVP: Returns a stub user. In production, verify JWT token.
    """
    # Stub implementation - always returns a user
    # In production, verify token and fetch user from database
    if token:
        # TODO: Verify JWT token
        pass
    
    return {
        "id": 1,
        "email": "user@example.com",
        "name": "Demo User"
    }


async def require_auth(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency that requires authentication.
    Use this on protected routes.
    """
    return current_user

