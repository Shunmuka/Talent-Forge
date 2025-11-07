from fastapi import FastAPI

from .routes import analyze, rewrite

app = FastAPI(title="Talent Forge API", version="0.0.1")


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


app.include_router(analyze.router)
app.include_router(rewrite.router)
# TODO: add middleware, auth, and telemetry when ready.
