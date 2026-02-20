from __future__ import annotations

from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)


class JobResponse(BaseModel):
    id: str
    title: str
    country: str
    description: str
