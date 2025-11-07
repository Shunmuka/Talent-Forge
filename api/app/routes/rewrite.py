from fastapi import APIRouter

from ..schemas.rewrite import RewriteResponse

router = APIRouter()


@router.post("/api/rewrite", response_model=RewriteResponse)
async def rewrite_bullet() -> RewriteResponse:
    """Static placeholder for rewrite assistance."""
    return RewriteResponse(
        original="Original bullet placeholder.",
        revised="Rewritten bullet emphasizing quantifiable impact.",
        rationale="TODO: explain rewrite reasoning based on JD context."
    )
