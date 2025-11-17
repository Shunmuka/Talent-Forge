# Talent Forge MVP - Demo Deck Outline (10 Slides)

## Slide 1: Problem & Target User (1 min)
- **Problem**: Job seekers struggle to tailor resumes to job descriptions
- **Pain Points**: 
  - Don't know what skills are missing
  - Bullet points aren't ATS-friendly
  - Time-consuming manual matching
- **Target User**: Job seekers applying to tech roles

## Slide 2: Solution Overview
- **What**: AI-powered resume analysis and rewriting tool
- **Key Features**:
  - Match score (0-100)
  - Skill gap identification
  - Evidence snippets
  - One-click bullet rewriting

## Slide 3: Live Demo - Upload & Analyze (2 min)
- Show: Upload resume (PDF) or paste text
- Show: Paste job description
- Show: Click "Analyze"
- Result: Score, gaps, evidence displayed

## Slide 4: Live Demo - Results View (1 min)
- Show: Score visualization
- Show: Top skill gaps with reasons
- Show: Evidence snippets linking resume to JD
- Show: Extracted bullets

## Slide 5: Live Demo - Rewrite Feature (2 min)
- Show: Click "Rewrite" on a bullet
- Show: Modal with original vs revised
- Show: Rationale explanation
- Show: Copy to clipboard

## Slide 6: Architecture Overview (1 min)
- **Frontend**: Next.js + TypeScript
- **Backend**: FastAPI (Python)
- **ML**: Sentence Transformers + Gemini API
- **Database**: PostgreSQL

## Slide 7: API Contract (1 min)
- Show: OpenAPI spec highlights
- Key endpoints: `/api/analyze`, `/api/rewrite`
- Response times: ≤5s target

## Slide 8: Quality Metrics
- **Latency**: ≤5s for typical inputs
- **Accuracy**: Top-5 gaps judged reasonable on 8/10 fixtures
- **Test Coverage**: Backend ≥70%, E2E happy path green

## Slide 9: Results & Metrics
- **MVP Scope**: Core analyze + rewrite flow
- **Out of Scope**: Multi-resume libraries, payments, analytics
- **Success Criteria**: All met ✅

## Slide 10: Next Steps
- **Immediate**: Production auth, rate limiting
- **Future**: Multi-resume libraries, exports, notifications
- **Scaling**: Caching, observability, performance optimization

---

## Demo Script Notes

### Setup (Before Demo)
1. Have 2-3 fresh resume/JD pairs ready
2. Ensure API is running and responsive
3. Test upload flow beforehand
4. Have backup plan if API is slow

### During Demo
- Keep it under 10 minutes
- Focus on user value, not technical details
- Show real examples, not placeholders
- Handle errors gracefully

### Q&A Prep
- Be ready to explain ML approach (embeddings + similarity)
- Discuss limitations (auth stub, no persistence)
- Mention future roadmap items
