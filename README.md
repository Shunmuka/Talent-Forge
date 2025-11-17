# Talent Forge MVP

A web application that analyzes resumes against job descriptions, identifies skill gaps, and provides AI-powered bullet point rewriting suggestions.

## Features

- 📄 **Resume Analysis**: Upload or paste resume, compare against job description
- 📊 **Match Scoring**: Get a 0-100 match score with semantic similarity
- 🔍 **Gap Identification**: See top skill gaps with explanations
- 📝 **Evidence Snippets**: View how your resume aligns with job requirements
- ✏️ **Bullet Rewriting**: One-click AI-powered bullet point improvements
- 🎯 **ATS-Friendly**: Rewritten bullets optimized for applicant tracking systems

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 15+ (optional for MVP, can run without DB)
- Gemini API key (for ML features)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Talent-Forge
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Install dependencies**
   ```bash
   make setup
   ```

4. **Start the application**
   ```bash
   # Start both frontend and backend
   make dev

   # Or start separately:
   make dev-api      # Backend on http://localhost:8000
   make dev-frontend # Frontend on http://localhost:3000
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
Talent-Forge/
├── api/                 # FastAPI backend
│   ├── app/
│   │   ├── routes/      # API endpoints
│   │   ├── schemas/     # Pydantic models
│   │   ├── services/    # Business logic
│   │   ├── models.py    # Database models
│   │   └── main.py      # FastAPI app
│   └── alembic/         # Database migrations
├── frontend/            # Next.js frontend
│   └── src/
│       ├── pages/       # Next.js pages
│       ├── lib/         # API client
│       └── styles/      # CSS/Tailwind
├── ml/                  # ML/Scoring module
│   └── scorer/         # Scoring functions
├── docs/                # Documentation
├── fixtures/            # Test data
└── infra/               # Infrastructure configs
```

## Development

### Backend

```bash
cd api
# Install dependencies
pip install -e . && pip install -e ".[dev]"

# Run tests
pytest

# Run server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
# Install dependencies
npm install

# Run dev server
npm run dev

# Run tests
npm run test
```

### Database (Optional)

```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Run migrations
cd api
alembic upgrade head
```

## API Endpoints

- `POST /api/analyze` - Analyze resume against job description
- `POST /api/rewrite` - Rewrite a bullet point
- `GET /healthz` - Health check

See `docs/API_CONTRACT.md` for full API documentation.

## Testing

```bash
# Run all tests
make test

# Backend tests only
cd api && pytest

# Frontend E2E tests
cd frontend && npm run test
```

## Documentation

- [System Design](./docs/SYSTEM_DESIGN_ONE_PAGER.md)
- [API Contract](./docs/API_CONTRACT.md)
- [Offboarding Guide](./docs/OFFBOARDING.md)
- [Demo Deck Outline](./docs/DEMO_DECK_OUTLINE.md)

## MVP Scope

### In Scope ✅
- Resume upload/paste + JD paste
- Match score (0-100)
- Top 10 skill gaps
- Evidence snippets
- Bullet extraction
- One-click bullet rewriting
- Basic UI with Tailwind CSS

### Out of Scope (Future)
- Multi-resume libraries
- Export functionality
- User accounts/persistence
- Analytics dashboard
- Payment integration
- Interview practice features

## Success Criteria

- ✅ Latency: `/api/analyze` ≤ 5s
- ✅ Quality: Top-5 gaps reasonable on 8/10 fixtures
- ✅ Rewrite: Returns stronger bullet with rationale
- ✅ Resilience: Graceful error handling
- ✅ Tests: Backend ≥70% coverage, E2E happy path

## Tech Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **ML**: Sentence Transformers, Google Gemini API
- **Database**: PostgreSQL
- **Testing**: Pytest, Playwright

## Contributing

This is an MVP project. See the rotation plan in the project documentation for contribution guidelines.

## License

See LICENSE file.

## Support

For issues or questions, please open an issue in the repository.
