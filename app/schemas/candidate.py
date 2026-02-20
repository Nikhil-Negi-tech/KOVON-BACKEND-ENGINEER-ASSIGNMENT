"""Pydantic schemas for candidate APIs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CandidateCreateRequest(BaseModel):
    """Payload for creating a candidate."""

    name: str = Field(min_length=1, max_length=200)
    skill_description: str = Field(min_length=1)
    experience: int = Field(ge=0, description="Years of professional experience")
    location: str = Field(min_length=1, max_length=100)


class CandidateResponse(BaseModel):
    """API response for candidate data."""

    id: str
    name: str
    skill_description: str
    experience: int
    location: str
