from fastapi import APIRouter

from ..schemas.analyze import AnalyzeResponse, AnalyzeGap, AnalyzeEvidence

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_resume() -> AnalyzeResponse:
    """Static placeholder for resume analysis."""
    return AnalyzeResponse(
        score=72,
        gaps=[AnalyzeGap(skill="GraphQL", reason="TODO: replace with scoring engine.")],
        evidence=[
            AnalyzeEvidence(
                resumeText="Sample resume text snippet.",
                jdText="Sample job description snippet."
            )
        ],
        bullets=["TODO: craft summary bullet once scoring works."]
    )
