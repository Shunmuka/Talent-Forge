# Talent Forge MVP - Quick Checklist

## 🚨 Critical Path (Must Complete)

### Backend API
- [ ] Add `AnalyzeRequest` schema (`resumeText?`, `resumeFileId?`, `jobDescription`)
- [ ] Add `RewriteRequest` schema (`original`, `context?`)
- [ ] Implement real `/api/analyze` endpoint (currently returns hardcoded data)
- [ ] Implement real `/api/rewrite` endpoint (currently returns hardcoded data)
- [ ] Add PDF/DOCX file upload handling
- [ ] Port text extraction from Flask app to FastAPI
- [ ] Add dependencies to `pyproject.toml` (FastAPI, Uvicorn, PyPDF2, python-docx, etc.)

### ML/Scoring Module
- [ ] Port embedding logic from `flask-app/main.py` to `ml/scorer/__init__.py`
- [ ] Implement `embed()` wrapper with caching
- [ ] Implement bullet splitter function
- [ ] Implement cosine similarity calculation
- [ ] Implement gap extraction logic
- [ ] Implement evidence span extraction
- [ ] Implement `rewrite_bullet()` function
- [ ] Add unit tests for ML functions

### Frontend
- [ ] Build `/analyze` page (upload/paste resume + paste JD)
- [ ] Build `/results` page (score, gaps, evidence, bullets)
- [ ] Implement rewrite modal with inline diff
- [ ] Wire up `frontend/src/lib/api.ts` to make real HTTP calls
- [ ] Add Tailwind CSS styling
- [ ] Add loading states and error handling
- [ ] Add accessibility features (labels, focus, keyboard nav)

### Database
- [ ] Create SQLAlchemy models (Users, Resumes, Analyses, Bullets)
- [ ] Set up Alembic migrations
- [ ] Configure database connection
- [ ] Complete `infra/scripts/bootstrap_db.sql`

### Authentication
- [ ] Implement Google OAuth (or stub for MVP)
- [ ] Add auth middleware
- [ ] Protect `/api/analyze` and `/api/rewrite` endpoints

## 🔧 Infrastructure & DevEx

### Makefile
- [ ] Implement `setup` target
- [ ] Implement `dev` target (orchestrate full stack)
- [ ] Implement `dev-frontend` target
- [ ] Implement `dev-api` target
- [ ] Implement `test` target
- [ ] Implement `lint` target
- [ ] Implement `seed` target

### Environment
- [ ] Create `.env.example` file
- [ ] Document all required environment variables

### Docker
- [ ] Complete `docker-compose.yml` (fill in commands)
- [ ] Verify Dockerfiles work correctly

## ✅ Testing

### Backend Tests
- [ ] Write FastAPI TestClient tests for endpoints
- [ ] Write unit tests for ML scorer (≥70% coverage target)
- [ ] Configure coverage reporting

### Frontend Tests
- [ ] Implement Playwright happy path E2E test
- [ ] Test upload → analyze → results → rewrite flow

## 📚 Documentation

- [ ] Complete `SYSTEM_DESIGN_ONE_PAGER.md`
- [ ] Complete `OFFBOARDING.md`
- [ ] Complete `DEMO_DECK_OUTLINE.md` (10 slides)
- [ ] Complete `API_CONTRACT.md`
- [ ] Update main `README.md` with setup instructions

## 🎨 Polish & Quality

- [ ] Add error handling throughout
- [ ] Add request validation
- [ ] Add rate limiting
- [ ] Add basic logging
- [ ] Mobile responsiveness
- [ ] Performance: embedding cache
- [ ] Input size limits (2-page resume, 1-page JD target)

## 📦 Dependencies to Add

### Backend (`api/pyproject.toml`)
```
fastapi
uvicorn[standard]
pydantic
sqlalchemy
alembic
psycopg2-binary
PyPDF2
python-docx
sentence-transformers
google-generativeai
python-multipart
```

### Frontend (`frontend/package.json`)
```
next
react
react-dom
typescript
tailwindcss
@tanstack/react-query
msw
playwright
```

---

## 🎯 Week 1 Focus
1. Port ML logic → `ml/scorer/`
2. Implement real `/api/analyze` endpoint
3. Build `/analyze` page UI
4. Set up database models

## 🎯 Week 2 Focus
1. Implement `/api/rewrite` endpoint
2. Build `/results` page + rewrite modal
3. Add tests and polish
4. Complete documentation

