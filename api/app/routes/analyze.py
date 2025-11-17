from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional

from ..schemas.analyze import AnalyzeResponse, AnalyzeGap, AnalyzeEvidence, AnalyzeRequest
from ..services.file_parser import extract_text_from_file, clean_text
from ml.scorer import (
    compute_match_score,
    extract_bullets,
    analyze_gaps,
    extract_evidence,
)

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    request: Optional[AnalyzeRequest] = None,
    resume_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
) -> AnalyzeResponse:
    """
    Analyze resume against job description.
    
    Accepts either:
    - JSON body with AnalyzeRequest
    - Form data with file upload or text paste
    """
    # Handle form data (file upload)
    if resume_file or resume_text or job_description:
        # Extract resume text
        if resume_file:
            try:
                resume_content = extract_text_from_file(resume_file)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")
        elif resume_text:
            resume_content = clean_text(resume_text)
        else:
            raise HTTPException(status_code=400, detail="Either resume_file or resume_text required")
        
        if not job_description:
            raise HTTPException(status_code=400, detail="job_description is required")
        
        jd_text = clean_text(job_description)
    
    # Handle JSON body
    elif request:
        if request.resumeFileId:
            # TODO: Load from database when file storage is implemented
            raise HTTPException(status_code=501, detail="File ID lookup not yet implemented")
        
        if not request.resumeText:
            raise HTTPException(status_code=400, detail="resumeText is required")
        
        resume_content = clean_text(request.resumeText)
        jd_text = clean_text(request.jobDescription)
    
    else:
        raise HTTPException(status_code=400, detail="Request body or form data required")
    
    # Validate inputs
    if not resume_content or len(resume_content) < 10:
        raise HTTPException(status_code=400, detail="Resume text is too short or empty")
    
    if not jd_text or len(jd_text) < 10:
        raise HTTPException(status_code=400, detail="Job description is too short or empty")
    
    try:
        # Compute match score
        score = compute_match_score(resume_content, jd_text)
        
        # Extract gaps
        gaps_data = analyze_gaps(resume_content, jd_text, max_gaps=10)
        gaps = [AnalyzeGap(skill=g["skill"], reason=g["reason"]) for g in gaps_data]
        
        # Extract evidence
        evidence_data = extract_evidence(resume_content, jd_text, max_evidence=10)
        evidence = [
            AnalyzeEvidence(resumeText=e["resumeText"], jdText=e["jdText"])
            for e in evidence_data
        ]
        
        # Extract bullets
        bullets = extract_bullets(resume_content, max_bullets=15)
        
        return AnalyzeResponse(
            score=score,
            gaps=gaps,
            evidence=evidence,
            bullets=bullets,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
