.PHONY: setup dev dev-frontend dev-api test lint typecheck format seed help

help:
	@echo "Talent Forge MVP - Available commands:"
	@echo "  make setup          - Initial setup (install dependencies)"
	@echo "  make dev            - Start full stack (frontend + backend)"
	@echo "  make dev-frontend    - Start frontend only"
	@echo "  make dev-api         - Start backend API only"
	@echo "  make test            - Run all tests"
	@echo "  make lint            - Lint code"
	@echo "  make typecheck       - Type check frontend"
	@echo "  make format          - Format code"
	@echo "  make seed            - Seed fixtures"

setup:
	@echo "Setting up Talent Forge..."
	@echo "Installing backend dependencies..."
	cd api && pip install -e . && pip install -e ".[dev]"
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Setup complete! Copy .env.example to .env and configure."

dev:
	@echo "Starting full stack..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop"
	@make dev-api & make dev-frontend

dev-frontend:
	@echo "Starting frontend dev server..."
	cd frontend && npm run dev

dev-api:
	@echo "Starting backend API server..."
	cd api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "Running tests..."
	@echo "Backend tests..."
	cd api && pytest
	@echo "Frontend tests..."
	cd frontend && npm run test

lint:
	@echo "Linting code..."
	@echo "Backend linting..."
	cd api && ruff check . || true
	@echo "Frontend linting..."
	cd frontend && npm run lint

typecheck:
	@echo "Type checking frontend..."
	cd frontend && npm run typecheck

format:
	@echo "Formatting code..."
	@echo "Backend formatting..."
	cd api && black . || true
	@echo "Frontend formatting..."
	cd frontend && npm run lint -- --fix || true

seed:
	@echo "Seeding fixtures..."
	@echo "TODO: Implement fixture seeding script"
	@echo "Fixtures are in fixtures/ directory"
