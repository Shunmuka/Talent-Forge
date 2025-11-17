# Talent Forge - Quick Start Guide

## 🚀 How to Run the Entire Application

This guide will help you get Talent Forge up and running in minutes.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 15+** (Optional - only needed if you want database features)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Verify Installation

```bash
python3 --version  # Should show Python 3.9 or higher
node --version     # Should show v18 or higher
npm --version      # Should show version number
```

---

## 🛠️ Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Shunmuka/Talent-Forge.git
cd Talent-Forge
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```bash
# Required for AI features
GEMINI_API_KEY=your-gemini-api-key-here

# Optional - Database (can skip for MVP)
DATABASE_URL=postgresql://tf_user:tf_pass@localhost:5432/talent_forge

# Frontend API URL
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Get your Gemini API key:**
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy and paste into `.env`

### 3. Install Dependencies

#### Backend Dependencies

```bash
cd api
pip install -e . && pip install -e ".[dev]"
cd ..
```

#### Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

**Or use the Makefile (recommended):**

```bash
make setup
```

---

## ▶️ Running the Application

### Option 1: Using Makefile (Easiest)

```bash
# Start both backend and frontend
make dev
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000

### Option 2: Manual Start

#### Start Backend

```bash
# From project root
cd api
PYTHONPATH=/Users/sriniketh/Talent-Forge:$PYTHONPATH uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or using the Makefile:

```bash
make dev-api
```

#### Start Frontend

```bash
# From project root
cd frontend
npm run dev
```

Or using the Makefile:

```bash
make dev-frontend
```

---

## 🌐 Access the Application

Once both servers are running:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/healthz

---

## ✅ Verify Everything Works

### Test Backend

```bash
curl http://localhost:8000/healthz
```

Should return:
```json
{"status": "ok", "version": "0.1.0"}
```

### Test Frontend

Open http://localhost:3000 in your browser. You should see the Talent Forge homepage.

### Test Full Flow

1. Go to http://localhost:3000
2. Upload a PDF resume or paste text
3. Paste a job description
4. Click "Analyze Resume"
5. View results with match score, gaps, and evidence
6. Click "Rewrite" on any bullet to get AI improvements

---

## 🛑 Stopping the Servers

Press `Ctrl+C` in the terminal where the servers are running.

Or use:

```bash
# Stop backend
pkill -f "uvicorn api.app.main:app"

# Stop frontend
pkill -f "next dev"
```

---

## 🐛 Troubleshooting

### Backend won't start

**Issue**: `ModuleNotFoundError` or missing dependencies
**Solution**: 
```bash
cd api
pip install -e . && pip install -e ".[dev]"
```

**Issue**: Port 8000 already in use
**Solution**: 
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill
```

### Frontend won't start

**Issue**: `npm: command not found`
**Solution**: Install Node.js from https://nodejs.org/

**Issue**: Port 3000 already in use
**Solution**: 
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill
```

**Issue**: Dependencies not installed
**Solution**:
```bash
cd frontend
npm install
```

### File upload fails

**Issue**: "Failed to fetch" error
**Solution**: 
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify file is PDF, DOCX, or TXT format
- File size must be under 16MB

### API key not working

**Issue**: Still seeing "API Configuration" gaps
**Solution**:
1. Verify `.env` file has `GEMINI_API_KEY=your-key`
2. Restart the backend server
3. Make sure `.env` is in the project root (not in `api/` folder)

### Database errors (if using database)

**Issue**: Database connection errors
**Solution**: 
- Make sure PostgreSQL is running
- Verify `DATABASE_URL` in `.env` is correct
- Run migrations: `cd api && alembic upgrade head`

---

## 📁 Project Structure

```
Talent-Forge/
├── api/                 # Backend (FastAPI)
│   ├── app/
│   │   ├── routes/      # API endpoints
│   │   ├── schemas/     # Request/Response models
│   │   └── services/    # Business logic
│   └── alembic/         # Database migrations
├── frontend/            # Frontend (Next.js)
│   └── src/
│       ├── pages/       # Next.js pages
│       └── lib/         # API client
├── ml/                  # ML/Scoring module
│   └── scorer/         # Scoring functions
├── docs/                # Documentation
├── fixtures/            # Test data
└── .env                 # Environment variables (not in git)
```

---

## 🔧 Development Commands

```bash
# Setup everything
make setup

# Run full stack
make dev

# Run only backend
make dev-api

# Run only frontend
make dev-frontend

# Run tests
make test

# Lint code
make lint

# Type check
make typecheck
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when backend is running)
- **System Design**: See `docs/SYSTEM_DESIGN_ONE_PAGER.md`
- **API Contract**: See `docs/API_CONTRACT.md`
- **Main README**: See `README.md`

---

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review the logs:
   - Backend: Check terminal output or `/tmp/backend.log`
   - Frontend: Check terminal output or browser console
3. Verify all prerequisites are installed
4. Make sure `.env` file is configured correctly

---

## ✨ Quick Test

After setup, test the API:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resumeText": "Software Engineer with Python experience",
    "jobDescription": "Senior Software Engineer with Python and React"
  }'
```

You should get a JSON response with score, gaps, evidence, and bullets!

---

**Happy coding! 🚀**

