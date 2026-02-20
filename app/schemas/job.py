"""Pydantic schemas for job APIs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    """Payload for creating a job."""

    title: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)


class JobResponse(BaseModel):
    """API response for job data."""

    id: str
    title: str
    country: str
    description: str
