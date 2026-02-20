from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.db.dependencies import get_matching_service
from app.schemas.candidate import CandidateCreateRequest, CandidateResponse
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    payload: CandidateCreateRequest,
    service: MatchingService = Depends(get_matching_service),
) -> CandidateResponse:
    return await service.create_candidate(payload)
