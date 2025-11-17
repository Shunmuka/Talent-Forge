from typing import List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request schema for resume analysis."""
    resumeText: Optional[str] = Field(None, description="Resume text (paste or extracted from file)")
    resumeFileId: Optional[str] = Field(None, description="ID of uploaded resume file")
    jobDescription: str = Field(..., description="Job description text", min_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "resumeText": "Software Engineer with 5 years of experience...",
                "jobDescription": "We are looking for a Senior Software Engineer..."
            }
        }


class AnalyzeGap(BaseModel):
    skill: str
    reason: str


class AnalyzeEvidence(BaseModel):
    resumeText: str
    jdText: str


class AnalyzeResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Match score (0-100)")
    gaps: List[AnalyzeGap] = Field(..., max_items=10, description="Top skill gaps")
    evidence: List[AnalyzeEvidence] = Field(..., description="Evidence snippets linking resume to JD")
    bullets: List[str] = Field(..., description="Extracted resume bullet points")
