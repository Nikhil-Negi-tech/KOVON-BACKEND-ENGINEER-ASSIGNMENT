"""Pydantic schemas for candidate-job matching APIs."""

from __future__ import annotations

from pydantic import BaseModel


class CandidateMatchResponse(BaseModel):
    """Single candidate match result for a job."""

    candidateId: str
    similarityScore: float
    experience: int


class MatchResultsResponse(BaseModel):
    """Top ranked candidates for a job."""

    jobId: str
    matches: list[CandidateMatchResponse]
