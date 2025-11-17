# Talent Forge MVP - Remaining Work Analysis

## Executive Summary

The repository has **basic scaffolding** in place but **most core functionality is missing**. The project structure follows the plan, but endpoints are placeholders, the frontend is empty, ML/scoring is not implemented in the FastAPI backend, and critical infrastructure pieces are incomplete.

**Note:** There's a working Flask app (`flask-app/`) and Streamlit prototype (`function.py`) with actual ML implementations that could be ported to FastAPI.

---

## ✅ What's Complete

### Project Structure
- ✅ Directory layout matches plan (`/api`, `/frontend`, `/ml`, `/infra`, `/docs`, `/fixtures`, `/openapi`)
- ✅ OpenAPI spec defined (`openapi/talent-forge.v1.yaml`)
- ✅ Basic Pydantic response schemas (`api/app/schemas/`)
- ✅ FastAPI skeleton with healthcheck (`api/app/main.py`)
- ✅ Next.js frontend skeleton (`frontend/`)
- ✅ MSW mock handlers defined (`frontend/src/mocks/handlers.ts`)
- ✅ Docker Compose structure (`infra/docker-compose.yml`)
- ✅ Documentation placeholders created
- ✅ Fixtures folder with sample data

### Prototype Code (Not Integrated)
- ✅ Flask app with working ML logic (`flask-app/main.py`)
- ✅ Streamlit prototype (`function.py`)
- ✅ PDF/DOCX parsing logic exists (in Flask app)
- ✅ Embedding + cosine similarity logic exists (in Flask app)
- ✅ Gap analysis logic exists (in Flask app)
- ✅ Bullet rewrite logic exists (in Flask app)

---

## ❌ Critical Missing Components

### 1. Backend (FastAPI) - HIGH PRIORITY

#### Request Schemas
- ❌ `AnalyzeRequest` schema missing (needs `resumeText?: string`, `resumeFileId?: string`, `jobDescription: string`)
- ❌ `RewriteRequest` schema missing (needs `original: string`, `context?: string`)
- ❌ Request validation not implemented

#### Endpoint Implementation
- ❌ `/api/analyze` returns hardcoded placeholder data
- ❌ `/api/rewrite` returns hardcoded placeholder data
- ❌ No integration with ML scorer module
- ❌ No file upload handling (PDF/DOCX)
- ❌ No text extraction from files
- ❌ No error handling or validation
- ❌ No rate limiting
- ❌ No request/response logging

#### Database Layer
- ❌ No database models (Users, Resumes, Analyses, Bullets)
- ❌ No migrations (Alembic or similar)
- ❌ No database connection setup
- ❌ No ORM (SQLAlchemy) configured
- ❌ Database initialization script is placeholder

#### Authentication
- ❌ Google OAuth not implemented
- ❌ No auth middleware
- ❌ No protected route guards
- ❌ No user session management

#### File Processing
- ❌ PDF parsing not integrated (exists in Flask but not FastAPI)
- ❌ DOCX parsing not integrated (exists in Flask but not FastAPI)
- ❌ No MIME type validation
- ❌ No file size limits
- ❌ No paste-text fallback handling

#### Dependencies
- ❌ `pyproject.toml` has no dependencies listed
- ❌ Missing: FastAPI, Uvicorn, Pydantic, SQLAlchemy, PyPDF2, python-docx, sentence-transformers, etc.

---

### 2. ML/Scoring Module - HIGH PRIORITY

#### Core Functions
- ❌ `ml/scorer/__init__.py` is empty placeholder
- ❌ No `embed()` wrapper function
- ❌ No embedding cache implementation
- ❌ No bullet splitter function
- ❌ No JD terms extraction
- ❌ No cosine similarity calculation
- ❌ No coverage-based scoring
- ❌ No gap extraction logic
- ❌ No evidence span extraction
- ❌ No `rewrite_bullet()` function
- ❌ No prompt template integration
- ❌ No unit tests for ML functions

**Note:** Logic exists in `flask-app/main.py` but needs to be refactored into `ml/scorer/` module.

---

### 3. Frontend (Next.js) - HIGH PRIORITY

#### Pages
- ❌ `/analyze` page is empty placeholder
  - Missing: File upload UI
  - Missing: Paste text option
  - Missing: JD paste textarea
  - Missing: Form validation
  - Missing: Loading states
  - Missing: Error handling
- ❌ `/results` page is empty placeholder
  - Missing: Score display
  - Missing: Gaps list rendering
  - Missing: Evidence snippets display
  - Missing: Bullets list
  - Missing: Rewrite modal
  - Missing: Inline diff view
  - Missing: Copy functionality

#### API Client
- ❌ `frontend/src/lib/api.ts` has placeholder functions that throw errors
- ❌ No actual HTTP calls to backend
- ❌ No error handling
- ❌ No request/response typing

#### UI/UX
- ❌ No Tailwind CSS styling
- ❌ No loading spinners/toasts
- ❌ No error messages
- ❌ No accessibility features (labels, focus, keyboard navigation)
- ❌ No mobile responsiveness
- ❌ No React Query integration (mentioned in plan)

#### Configuration
- ❌ `package.json` scripts are all TODOs
- ❌ No actual Next.js dependencies installed
- ❌ No TypeScript configuration validation

---

### 4. Testing - MEDIUM PRIORITY

#### Backend Tests
- ❌ `test_health.py` is placeholder (just `assert True`)
- ❌ No FastAPI TestClient tests
- ❌ No unit tests for ML scorer
- ❌ No integration tests for endpoints
- ❌ Coverage not configured
- ❌ Coverage threshold not set (target: ≥70%)

#### Frontend Tests
- ❌ E2E test skeleton exists but empty
- ❌ No Playwright/Cypress implementation
- ❌ No happy path test
- ❌ No unit tests for components

---

### 5. DevOps & Developer Experience - MEDIUM PRIORITY

#### Makefile
- ❌ All targets are TODOs:
  - `setup` - not implemented
  - `dev` - not implemented
  - `dev-frontend` - not implemented
  - `dev-api` - not implemented
  - `test` - not implemented
  - `lint` - not implemented
  - `typecheck` - not implemented
  - `format` - not implemented
  - `seed` - not implemented

#### Environment Setup
- ❌ No `.env.example` file
- ❌ No environment variable documentation
- ❌ No local dev setup guide

#### Docker
- ❌ Docker Compose has TODOs:
  - API service command not filled
  - Frontend service command not filled
  - Database initialization not configured
- ❌ Dockerfiles exist but may need review

#### CI/CD
- ❌ No CI scripts (GitHub Actions, etc.)
- ❌ No automated test runs
- ❌ No deployment automation

---

### 6. Documentation - LOW PRIORITY (but required)

#### System Design
- ❌ `SYSTEM_DESIGN_ONE_PAGER.md` is placeholder (just "TODO")

#### Offboarding
- ❌ `OFFBOARDING.md` is placeholder (just "TODO")

#### Demo Deck
- ❌ `DEMO_DECK_OUTLINE.md` is placeholder (just "TODO")

#### API Contract
- ❌ `API_CONTRACT.md` is placeholder (just "TODO")

#### README
- ❌ Main `README.md` says "How to run: coming soon"

---

## 📋 Detailed Task Breakdown

### Week 1 Tasks (Critical Path)

#### Day 1 (Kickoff) - **NOT DONE**
- [ ] Complete OpenAPI spec with request schemas
- [ ] Implement MSW mocks matching OpenAPI (partially done, needs request body)
- [ ] Create `.env.example` with all required variables
- [ ] Add 3 resume + 3 JD fixtures (2 JDs exist, need 1 more + 3 resumes)
- [ ] Set up Makefile targets for local dev

#### Rotation A (Tue-Wed) - **NOT DONE**

**Frontend (Surya)**
- [ ] Build `/analyze` page with upload/paste UI
- [ ] Connect to MSW mocks
- [ ] Render score/gaps placeholders

**Backend (Taher)**
- [ ] Add FastAPI dependencies to `pyproject.toml`
- [ ] Set up SQLAlchemy models (Users, Resumes, Analyses, Bullets)
- [ ] Create Alembic migrations
- [ ] Implement auth stub (placeholder for Google OAuth)
- [ ] Wire up database connection

**ML/Scoring (Aayush)**
- [ ] Port embedding logic from Flask to `ml/scorer/`
- [ ] Implement `embed()` wrapper
- [ ] Implement bullet splitter
- [ ] Implement cosine similarity
- [ ] Write unit tests

**DevEx/Docs (Sriniketh)**
- [ ] Implement Makefile targets
- [ ] Create local dev guide
- [ ] Seed fixtures script
- [ ] Set up E2E test skeleton (Playwright)

#### Rotation B (Thu-Fri) - **NOT DONE**

**Backend (Surya)**
- [ ] Implement real `/api/analyze` endpoint
- [ ] Integrate PDF/DOCX parsing (port from Flask)
- [ ] Add file upload handling
- [ ] Implement paste-text fallback

**ML/Scoring (Taher)**
- [ ] Implement gap extraction
- [ ] Implement evidence span extraction
- [ ] Add explanation strings

**DevEx/Docs (Aayush)**
- [ ] Implement Playwright happy path test
- [ ] Wire up coverage threshold

**Frontend (Sriniketh)**
- [ ] Build `/results` page
- [ ] Implement rewrite modal scaffold
- [ ] Connect to real API (replace mocks)

### Week 2 Tasks

#### Rotation C (Mon-Tue) - **NOT DONE**

**ML/Scoring (Surya)**
- [ ] Implement rewrite prompt template
- [ ] Create golden set (10 bullets)
- [ ] Implement `rewrite_bullet()` function

**Frontend (Taher)**
- [ ] Complete rewrite modal
- [ ] Add inline diff view
- [ ] Add copy functionality
- [ ] Switch from mocks to real API

**Backend (Aayush)**
- [ ] Implement real `/api/rewrite` endpoint
- [ ] Add validation
- [ ] Add simple rate limits

**DevEx/Docs (Sriniketh)**
- [ ] Complete system design one-pager
- [ ] Set up bug triage process
- [ ] Create test matrix

#### Rotation D (Wed-Thu) - **NOT DONE**

**DevEx/Perf (Surya)**
- [ ] Implement embedding cache per resume/JD
- [ ] Add basic logging

**Backend (Taher)**
- [ ] Harden parser (MIME checks, size caps)
- [ ] Add error typing
- [ ] Complete OpenAPI docs

**ML/Scoring (Aayush)**
- [ ] Improve evidence precision
- [ ] Test on 8/10 fixtures for plausibility

**Frontend (Sriniketh)**
- [ ] A11y pass (labels, focus, keyboard)
- [ ] Error path handling
- [ ] Mobile responsiveness

---

## 🔧 Quick Wins (Can Start Immediately)

1. **Port ML Logic**: Copy functions from `flask-app/main.py` to `ml/scorer/__init__.py`
2. **Add Request Schemas**: Create `AnalyzeRequest` and `RewriteRequest` in `api/app/schemas/`
3. **Implement Makefile**: Add basic `dev`, `dev-frontend`, `dev-api` targets
4. **Create .env.example**: Document all required environment variables
5. **Wire Frontend API Client**: Replace throw statements with actual fetch calls
6. **Build Analyze Page**: Create basic form with file upload and textarea
7. **Add Dependencies**: Fill in `pyproject.toml` and `package.json` with required packages

---

## 🚨 Blockers & Dependencies

1. **ML Module Must Be Done First**: Backend endpoints can't be implemented without ML scorer
2. **Database Models Needed**: Can't implement file storage or analysis history without DB
3. **Auth Can Be Stubbed**: Can use placeholder auth initially, implement Google OAuth later
4. **Frontend Depends on Backend**: Can use mocks initially, but need real API for final integration

---

## 📊 Completion Estimate

- **Overall Progress**: ~15-20% complete
- **Backend**: ~10% (skeleton only)
- **Frontend**: ~5% (placeholders only)
- **ML/Scoring**: ~0% (empty, but logic exists in Flask app)
- **DevOps**: ~20% (structure exists, implementation missing)
- **Documentation**: ~10% (placeholders exist)
- **Testing**: ~5% (skeletons exist)

---

## 🎯 Recommended Next Steps

1. **Immediate (Day 1)**:
   - Port ML logic from Flask to `ml/scorer/`
   - Add request schemas
   - Implement Makefile basics
   - Create `.env.example`

2. **Week 1 Priority**:
   - Implement real `/api/analyze` endpoint
   - Build `/analyze` page UI
   - Set up database models
   - Wire up ML scorer to backend

3. **Week 2 Priority**:
   - Implement `/api/rewrite` endpoint
   - Build `/results` page and rewrite modal
   - Add tests and polish
   - Complete documentation

---

## 📝 Notes

- The Flask app (`flask-app/`) appears to be a working prototype that should be ported to FastAPI
- The Streamlit app (`function.py`) also has working logic that can be reused
- Consider whether to keep Flask app as reference or remove it after porting
- The OpenAPI spec is well-defined and should be the source of truth for API contracts

