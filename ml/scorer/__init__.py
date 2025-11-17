"""ML/Scoring module for resume analysis and bullet rewriting."""
import os
import re
from typing import List, Tuple, Dict, Optional
from functools import lru_cache

import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import torch

# Initialize Gemini model
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    _gemini_model = genai.GenerativeModel("gemini-2.5-flash")
else:
    _gemini_model = None

# Global embedder cache
_embedder: Optional[SentenceTransformer] = None


def get_embedder() -> SentenceTransformer:
    """Get or initialize the sentence transformer embedder (cached)."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


@lru_cache(maxsize=100)
def embed(text: str) -> torch.Tensor:
    """
    Generate embedding for text with caching.
    
    Args:
        text: Input text to embed
        
    Returns:
        Embedding tensor
    """
    embedder = get_embedder()
    return embedder.encode(text, convert_to_tensor=True)


def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace."""
    return re.sub(r"\s+", " ", text).strip()


def extract_bullets(text: str, max_bullets: int = 15) -> List[str]:
    """
    Extract bullet points from resume text.
    
    Args:
        text: Resume text
        max_bullets: Maximum number of bullets to return
        
    Returns:
        List of extracted bullet points
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    bullets = []
    
    for line in lines:
        line = line.strip()
        # Match bullet starters or continuation lines (lowercase start suggests bullet)
        if re.match(r"^[-•*]\s", line) or (len(line) > 20 and line[0].islower()):
            clean_bullet = re.sub(r"^[-•*\s]+", "", line).strip()
            if len(clean_bullet) > 15:
                bullets.append(clean_bullet)
    
    return bullets[:max_bullets]


def compute_match_score(resume: str, job_description: str) -> int:
    """
    Calculate semantic similarity score between resume and job description.
    
    Args:
        resume: Resume text
        job_description: Job description text
        
    Returns:
        Match score (0-100)
    """
    resume_clean = clean_text(resume)
    jd_clean = clean_text(job_description)
    
    # Use cached embeddings
    r_emb = embed(resume_clean)
    j_emb = embed(jd_clean)
    
    # Compute cosine similarity
    sim = util.cos_sim(r_emb, j_emb)[0][0].item()
    
    # Convert to 0-100 scale
    score = round(sim * 100)
    return max(0, min(100, score))  # Clamp to 0-100


def extract_jd_terms(job_description: str) -> List[str]:
    """
    Extract key terms/skills from job description.
    
    Args:
        job_description: Job description text
        
    Returns:
        List of key terms
    """
    # Simple extraction - look for common tech terms, skills
    # This is a simplified version; could be enhanced with NER
    text = job_description.lower()
    common_terms = [
        "python", "javascript", "react", "node", "aws", "docker", "kubernetes",
        "sql", "postgresql", "mongodb", "redis", "graphql", "rest", "api",
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "agile", "scrum", "ci/cd", "git", "github", "gitlab"
    ]
    
    found_terms = [term for term in common_terms if term in text]
    return found_terms[:10]  # Return top 10


def analyze_gaps(resume: str, job_description: str, max_gaps: int = 10) -> List[Dict[str, str]]:
    """
    Identify gaps between resume and job description.
    
    Args:
        resume: Resume text
        job_description: Job description text
        max_gaps: Maximum number of gaps to return
        
    Returns:
        List of gap dictionaries with 'skill' and 'reason' keys
    """
    if not _gemini_model:
        # Fallback if Gemini not configured - use simple keyword-based analysis
        # Extract key terms from JD that might be missing
        jd_lower = job_description.lower()
        resume_lower = resume.lower()
        
        # Common tech skills to check
        common_skills = [
            "python", "javascript", "react", "node.js", "aws", "docker", 
            "kubernetes", "sql", "postgresql", "mongodb", "graphql", 
            "typescript", "java", "go", "rust", "terraform", "ci/cd"
        ]
        
        missing_skills = []
        for skill in common_skills:
            if skill in jd_lower and skill not in resume_lower:
                missing_skills.append(skill.title())
        
        if missing_skills:
            return [
                {
                    "skill": skill,
                    "reason": f"Job requires {skill} but it's not mentioned in your resume"
                }
                for skill in missing_skills[:max_gaps]
            ]
        
        # If no obvious gaps found, return a helpful message
        return [{
            "skill": "Configuration Note",
            "reason": "Gemini API key not configured. Add GEMINI_API_KEY to .env for AI-powered gap analysis. Basic keyword matching used instead."
        }]
    
    resume_clean = clean_text(resume)[:3000]  # Limit input size
    jd_clean = clean_text(job_description)[:3000]
    
    prompt = f"""You are a resume expert. Compare the resume and job description below.

Identify 3-10 critical gaps where the resume is missing important skills, tools, technologies, certifications, or experience mentioned in the job description.

For each gap, provide:
1. The missing skill/requirement
2. A brief reason why it's important for this role

Format your response as a bulleted list. Each bullet should be on its own line starting with a dash.
Each bullet should have the format: "Skill Name: Reason why it's needed"

Resume:
{resume_clean}

Job Description:
{jd_clean}
"""
    
    try:
        response = _gemini_model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split("\n")
        gaps = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith("-") or line.startswith("•") or line.startswith("*")):
                clean_line = re.sub(r"^[-•*]\s*", "", line).strip()
                
                # Parse "Skill: Reason" format
                if ":" in clean_line:
                    parts = clean_line.split(":", 1)
                    skill = parts[0].strip()
                    reason = parts[1].strip() if len(parts) > 1 else "Missing requirement"
                else:
                    # Fallback: use first part as skill, rest as reason
                    words = clean_line.split()
                    if len(words) > 5:
                        skill = " ".join(words[:3])
                        reason = " ".join(words[3:])
                    else:
                        skill = clean_line[:50]
                        reason = "Missing requirement"
                
                if len(skill) > 5 and len(reason) > 10:
                    gaps.append({"skill": skill, "reason": reason})
        
        # Fallback if parsing failed
        if not gaps:
            gaps = [
                {"skill": "Review Required", "reason": "Unable to automatically identify gaps. Please review job requirements manually."}
            ]
        
        return gaps[:max_gaps]
    except Exception as e:
        return [{"skill": "Analysis Error", "reason": f"Error analyzing gaps: {str(e)}"}]


def extract_evidence(resume: str, job_description: str, max_evidence: int = 10) -> List[Dict[str, str]]:
    """
    Extract evidence snippets linking resume to job description.
    
    Args:
        resume: Resume text
        job_description: Job description text
        max_evidence: Maximum number of evidence pairs to return
        
    Returns:
        List of evidence dictionaries with 'resumeText' and 'jdText' keys
    """
    resume_clean = clean_text(resume)
    jd_clean = clean_text(job_description)
    
    # Simple approach: find sentences with common keywords
    # More sophisticated: use embeddings to find similar sentences
    resume_sentences = [s.strip() for s in re.split(r"[.!?]\s+", resume_clean) if len(s.strip()) > 20]
    jd_sentences = [s.strip() for s in re.split(r"[.!?]\s+", jd_clean) if len(s.strip()) > 20]
    
    evidence = []
    
    # Find sentences with semantic similarity
    if len(resume_sentences) > 0 and len(jd_sentences) > 0:
        # Sample approach: take first few sentences that mention common terms
        jd_terms = extract_jd_terms(jd_clean)
        
        for r_sent in resume_sentences[:20]:  # Limit search
            for term in jd_terms[:5]:  # Check top terms
                if term.lower() in r_sent.lower():
                    # Find matching JD sentence
                    for j_sent in jd_sentences[:20]:
                        if term.lower() in j_sent.lower():
                            evidence.append({
                                "resumeText": r_sent[:200],  # Limit length
                                "jdText": j_sent[:200]
                            })
                            break
                    break
            
            if len(evidence) >= max_evidence:
                break
    
    # Fallback if no evidence found
    if not evidence:
        evidence = [{
            "resumeText": resume_clean[:200] if resume_clean else "Resume content",
            "jdText": jd_clean[:200] if jd_clean else "Job description content"
        }]
    
    return evidence[:max_evidence]


def rewrite_bullet(original: str, job_description: str, context: Optional[str] = None) -> Dict[str, str]:
    """
    Rewrite a resume bullet point to better match job description.
    
    Args:
        original: Original bullet point text
        job_description: Job description text
        context: Optional context (e.g., full resume)
        
    Returns:
        Dictionary with 'original', 'revised', and 'rationale' keys
    """
    if not _gemini_model:
        return {
            "original": original,
            "revised": original,  # No change if API not available
            "rationale": "API not configured"
        }
    
    jd_clean = clean_text(job_description)[:1500]  # Limit input
    context_text = f"\n\nContext (full resume):\n{clean_text(context)[:500]}" if context else ""
    
    prompt = f"""Rewrite this resume bullet point to better match the job description. 

Requirements:
- Use strong action verbs (e.g., "Led", "Designed", "Implemented", "Optimized")
- Include quantifiable metrics when possible (numbers, percentages, timeframes)
- Mirror language and terminology from the job description
- Keep it concise (under 120 characters if possible)
- Make it ATS-friendly (avoid special characters, use standard formatting)

Original Bullet:
{original}

Job Description:
{jd_clean}{context_text}

Provide:
1. The rewritten bullet point
2. A brief rationale explaining the improvements (1-2 sentences)

Format:
Rewritten: [your rewritten bullet]
Rationale: [explanation]
"""
    
    try:
        response = _gemini_model.generate_content(prompt)
        text = response.text.strip()
        
        # Parse response
        revised = original  # Default fallback
        rationale = "Rewritten to better match job requirements."
        
        # Try to extract rewritten bullet and rationale
        if "Rewritten:" in text:
            parts = text.split("Rewritten:", 1)
            if len(parts) > 1:
                rewritten_part = parts[1]
                if "Rationale:" in rewritten_part:
                    revised = rewritten_part.split("Rationale:")[0].strip()
                    rationale = rewritten_part.split("Rationale:")[1].strip()
                else:
                    revised = rewritten_part.strip()
        elif "Rationale:" in text:
            parts = text.split("Rationale:", 1)
            revised = parts[0].strip() if parts[0] else original
            rationale = parts[1].strip() if len(parts) > 1 else "Rewritten to better match job requirements."
        else:
            # Use first line as revised, rest as rationale
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if lines:
                revised = lines[0][:150]  # Limit length
                if len(lines) > 1:
                    rationale = " ".join(lines[1:3])[:200]
        
        # Clean up revised bullet
        revised = re.sub(r"^[-•*]\s*", "", revised).strip()
        if len(revised) > 150:
            revised = revised[:140] + "..."
        
        return {
            "original": original,
            "revised": revised,
            "rationale": rationale[:300]  # Limit rationale length
        }
    except Exception as e:
        return {
            "original": original,
            "revised": original,
            "rationale": f"Error during rewrite: {str(e)}"
        }
