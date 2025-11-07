from typing import List

from pydantic import BaseModel


class AnalyzeGap(BaseModel):
    skill: str
    reason: str


class AnalyzeEvidence(BaseModel):
    resumeText: str
    jdText: str


class AnalyzeResponse(BaseModel):
    score: int
    gaps: List[AnalyzeGap]
    evidence: List[AnalyzeEvidence]
    bullets: List[str]
