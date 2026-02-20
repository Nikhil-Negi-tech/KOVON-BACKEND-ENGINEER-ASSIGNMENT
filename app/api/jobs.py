from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.dependencies import get_matching_service
from app.schemas.job import JobCreateRequest, JobResponse
from app.schemas.matching import MatchResultsResponse
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreateRequest,
    service: MatchingService = Depends(get_matching_service),
) -> JobResponse:
    return await service.create_job(payload)


@router.get("/{job_id}/match", response_model=MatchResultsResponse)
async def match_candidates(
    job_id: str,
    service: MatchingService = Depends(get_matching_service),
) -> MatchResultsResponse:
    try:
        return await service.match_candidates_for_job(job_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
