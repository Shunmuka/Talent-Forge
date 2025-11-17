from fastapi import APIRouter, HTTPException

from ..schemas.rewrite import RewriteRequest, RewriteResponse
from ml.scorer import rewrite_bullet

router = APIRouter()


@router.post("/api/rewrite", response_model=RewriteResponse)
async def rewrite_bullet_endpoint(request: RewriteRequest) -> RewriteResponse:
    """
    Rewrite a resume bullet point to better match job description.
    """
    if not request.original or len(request.original.strip()) < 5:
        raise HTTPException(status_code=400, detail="Original bullet text is too short")
    
    try:
        result = rewrite_bullet(
            original=request.original,
            job_description=request.context or "",
            context=request.context,
        )
        
        return RewriteResponse(
            original=result["original"],
            revised=result["revised"],
            rationale=result["rationale"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rewrite error: {str(e)}")
