# Quick Setup Script

## One-Command Setup (macOS/Linux)

```bash
# Run this from the project root
./docs/quick-start/setup.sh
```

## Manual Setup Steps

### 1. Install Prerequisites

```bash
# Check Python
python3 --version  # Need 3.9+

# Check Node.js
node --version     # Need 18+

# Install Node.js if missing (macOS with Homebrew)
brew install node
```

### 2. Install Dependencies

```bash
# Backend
cd api
pip install -e . && pip install -e ".[dev]"
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-key-here
```

### 4. Start Servers

```bash
# Terminal 1 - Backend
cd api
PYTHONPATH=..:$PYTHONPATH uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Access Application

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

