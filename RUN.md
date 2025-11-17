# 🚀 How to Run Talent Forge

**Quick Start**: See [docs/quick-start/QUICK_START.md](docs/quick-start/QUICK_START.md) for 5-minute setup.

---

## Prerequisites

- Python 3.9+
- Node.js 18+
- Gemini API key (get from https://aistudio.google.com/app/apikey)

## Setup

```bash
# 1. Install dependencies
make setup

# 2. Configure environment
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your-key-here

# 3. Start application
make dev
```

## Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Detailed Instructions

For complete setup instructions, troubleshooting, and more, see:
- **[Quick Start Guide](docs/quick-start/README.md)** - Complete setup guide
- **[Common Issues](docs/quick-start/COMMON_ISSUES.md)** - Troubleshooting
- **[Quick Start (5 min)](docs/quick-start/QUICK_START.md)** - Fastest way to get running

## Commands

```bash
make setup      # Install all dependencies
make dev        # Start both frontend and backend
make dev-api    # Start only backend
make dev-frontend # Start only frontend
make test       # Run tests
```

---

**That's it!** Open http://localhost:3000 and start analyzing resumes! 🎉

