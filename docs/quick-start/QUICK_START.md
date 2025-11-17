# ⚡ Quick Start - 5 Minutes

Get Talent Forge running in 5 minutes!

## Step 1: Prerequisites (2 min)

```bash
# Check you have Python and Node.js
python3 --version  # Need 3.9+
node --version     # Need 18+

# If missing Node.js (macOS):
brew install node
```

## Step 2: Setup (1 min)

```bash
# Clone and enter
git clone https://github.com/Shunmuka/Talent-Forge.git
cd Talent-Forge

# Install dependencies
make setup
# OR manually:
# cd api && pip install -e . && cd ..
# cd frontend && npm install && cd ..
```

## Step 3: Configure (1 min)

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get key from: https://aistudio.google.com/app/apikey
# Add: GEMINI_API_KEY=your-key-here
```

## Step 4: Run (1 min)

```bash
# Start everything
make dev

# OR start separately:
# Terminal 1: make dev-api
# Terminal 2: make dev-frontend
```

## Step 5: Use It!

1. Open http://localhost:3000
2. Upload resume or paste text
3. Paste job description
4. Click "Analyze Resume"
5. See results!

---

## 🎯 That's It!

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🛑 To Stop

Press `Ctrl+C` in the terminal, or:

```bash
pkill -f uvicorn
pkill -f "next dev"
```

---

## ❓ Problems?

See `COMMON_ISSUES.md` for troubleshooting.

