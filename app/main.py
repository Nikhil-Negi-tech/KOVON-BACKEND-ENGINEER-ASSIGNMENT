"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.candidates import router as candidates_router
from app.api.jobs import router as jobs_router
from app.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}


app.include_router(candidates_router)
app.include_router(jobs_router)
