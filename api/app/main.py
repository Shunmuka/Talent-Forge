from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import analyze, rewrite

# Database import is optional for MVP
try:
    from .database import init_db
except ImportError:
    init_db = None

app = FastAPI(
    title="Talent Forge API",
    version="0.1.0",
    description="MVP API for resume analysis and rewriting",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    if init_db:
        # init_db()  # Uncomment when database is ready
        pass


@app.get("/healthz")
async def healthz():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


# Include routers
app.include_router(analyze.router)
app.include_router(rewrite.router)
