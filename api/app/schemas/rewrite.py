from pydantic import BaseModel


class RewriteResponse(BaseModel):
    original: str
    revised: str
    rationale: str
