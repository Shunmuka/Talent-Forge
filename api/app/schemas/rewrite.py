from typing import Optional

from pydantic import BaseModel, Field


class RewriteRequest(BaseModel):
    """Request schema for bullet rewriting."""
    original: str = Field(..., description="Original bullet point text", min_length=5)
    context: Optional[str] = Field(None, description="Optional context (e.g., full resume or job description)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "original": "Worked on software projects",
                "context": "Full resume text or job description for context"
            }
        }


class RewriteResponse(BaseModel):
    original: str
    revised: str
    rationale: str
