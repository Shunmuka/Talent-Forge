#!/bin/bash

# Talent Forge Quick Setup Script

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           Talent Forge - Quick Setup                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install node
    else
        echo "❌ Please install Node.js from https://nodejs.org/"
        exit 1
    fi
fi

echo "✅ Prerequisites check passed"
echo ""

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd api
pip install -e . && pip install -e ".[dev]" || {
    echo "⚠️  Using pip3 instead of pip..."
    pip3 install -e . && pip3 install -e ".[dev]"
}
cd ..
echo "✅ Backend dependencies installed"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..
echo "✅ Frontend dependencies installed"
echo ""

# Setup .env file
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file from .env.example"
    else
        echo "GEMINI_API_KEY=your-api-key-here" > .env
        echo "DATABASE_URL=postgresql://tf_user:tf_pass@localhost:5432/talent_forge" >> .env
        echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" >> .env
        echo "✅ Created .env file"
    fi
else
    echo "✅ .env file already exists"
fi

if ! grep -q "GEMINI_API_KEY=" .env || grep -q "your-api-key-here" .env; then
    echo ""
    echo "⚠️  IMPORTANT: Add your Gemini API key to .env file"
    echo "   1. Get key from: https://aistudio.google.com/app/apikey"
    echo "   2. Edit .env and replace 'your-api-key-here' with your actual key"
    echo ""
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete!                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the application:"
echo "   make dev"
echo ""
echo "   OR"
echo ""
echo "   Terminal 1: make dev-api"
echo "   Terminal 2: make dev-frontend"
echo ""
echo "🌐 Then open: http://localhost:3000"
echo ""
