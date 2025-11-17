# Talent Forge MVP - System Design One Pager

## Overview
Talent Forge is a web application that analyzes resumes against job descriptions, identifies skill gaps, and provides AI-powered bullet point rewriting suggestions.

## Architecture

### Components

1. **Frontend (Next.js)**
   - React-based UI with TypeScript
   - Tailwind CSS for styling
   - Pages: `/` (analyze), `/results` (results view)
   - API client for backend communication

2. **Backend API (FastAPI)**
   - Python-based REST API
   - Endpoints: `/api/analyze`, `/api/rewrite`
   - File upload handling (PDF/DOCX)
   - Database integration (PostgreSQL)

3. **ML/Scoring Module**
   - Sentence transformers for embeddings
   - Cosine similarity for matching
   - Gemini API for gap analysis and rewriting
   - Caching for embeddings

4. **Database (PostgreSQL)**
   - Users, Resumes, Analyses, BulletRewrites tables
   - SQLAlchemy ORM
   - Alembic migrations

## Data Flow

1. **Analyze Flow:**
   - User uploads/pastes resume + JD → Frontend
   - Frontend → POST `/api/analyze` → Backend
   - Backend extracts text (if file) → ML scorer
   - ML scorer: embeddings → similarity → gaps → evidence → bullets
   - Backend → Frontend (JSON response)
   - Frontend renders results

2. **Rewrite Flow:**
   - User clicks "Rewrite" on bullet → Frontend
   - Frontend → POST `/api/rewrite` → Backend
   - Backend → ML scorer (Gemini API)
   - ML scorer returns revised bullet + rationale
   - Backend → Frontend
   - Frontend shows modal with diff

## Key Design Decisions

- **Embedding Cache**: LRU cache for embeddings to reduce API calls
- **File Size Limits**: 16MB max for uploads
- **Input Truncation**: Resume/JD truncated to 3000 chars for gap analysis
- **Error Handling**: Graceful fallbacks for parsing failures
- **CORS**: Enabled for localhost:3000 (Next.js dev)

## Scaling Considerations

- **Latency Target**: ≤5s for analyze endpoint
- **Caching**: Embeddings cached per text input
- **Database**: Lightweight schema, minimal queries for MVP
- **API Rate Limits**: Simple rate limiting on rewrite endpoint (future)

## Security

- **Auth**: Stub for MVP, Google OAuth planned
- **File Validation**: MIME type checks, size limits
- **Input Sanitization**: Text cleaning, length limits
- **CORS**: Restricted origins

## Deployment

- **Frontend**: Vercel (Next.js)
- **Backend**: Render/Fly.io (FastAPI)
- **Database**: Managed PostgreSQL
- **Environment**: Docker Compose for local dev
