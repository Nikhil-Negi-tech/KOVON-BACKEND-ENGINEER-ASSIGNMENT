from __future__ import annotations

from pydantic import BaseModel


class CandidateMatchResponse(BaseModel):
    candidateId: str
    similarityScore: float
    experience: int


class MatchResultsResponse(BaseModel):
    jobId: str
    matches: list[CandidateMatchResponse]
