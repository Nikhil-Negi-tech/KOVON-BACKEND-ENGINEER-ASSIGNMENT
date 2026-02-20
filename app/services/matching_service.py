"""Core orchestration service for candidate-job semantic matching."""

from __future__ import annotations

from uuid import uuid4

from app.config import settings
from app.db.repositories import CandidateRepository, JobRepository
from app.db.vector_store import FaissVectorStore
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.candidate import CandidateCreateRequest, CandidateResponse
from app.schemas.job import JobCreateRequest, JobResponse
from app.schemas.matching import CandidateMatchResponse, MatchResultsResponse
from app.services.embedding_service import EmbeddingService


class MatchingService:
    """Handles candidate/job creation and semantic matching operations."""

    def __init__(
        self,
        candidate_repository: CandidateRepository,
        job_repository: JobRepository,
        vector_store: FaissVectorStore,
        embedding_service: EmbeddingService,
    ) -> None:
        self._candidate_repository = candidate_repository
        self._job_repository = job_repository
        self._vector_store = vector_store
        self._embedding_service = embedding_service

    async def create_candidate(self, payload: CandidateCreateRequest) -> CandidateResponse:
        """Create a candidate, embed skills text, and store vector."""
        candidate = Candidate(
            id=str(uuid4()),
            name=payload.name,
            skill_description=payload.skill_description,
            experience=payload.experience,
            location=payload.location,
        )

        embedding = await self._embedding_service.embed_text(candidate.skill_description)
        self._candidate_repository.add(candidate)
        self._vector_store.add_candidate(candidate.id, embedding)

        return CandidateResponse(
            id=candidate.id,
            name=candidate.name,
            skill_description=candidate.skill_description,
            experience=candidate.experience,
            location=candidate.location,
        )

    async def create_job(self, payload: JobCreateRequest) -> JobResponse:
        """Create a job, embed description text, and store vector."""
        job = Job(
            id=str(uuid4()),
            title=payload.title,
            country=payload.country,
            description=payload.description,
        )

        embedding = await self._embedding_service.embed_text(job.description)
        self._job_repository.add(job)
        self._vector_store.add_job(job.id, embedding)

        return JobResponse(
            id=job.id,
            title=job.title,
            country=job.country,
            description=job.description,
        )

    async def match_candidates_for_job(self, job_id: str) -> MatchResultsResponse:
        """Return top ranked candidates for a job using cosine similarity and experience tie-break."""
        job = self._job_repository.get(job_id)
        if job is None:
            raise KeyError(f"Job '{job_id}' not found.")
        job_embedding = self._vector_store.get_job_embedding(job_id)
        if job_embedding is None:
            raise ValueError(f"No embedding found for job '{job_id}'.")

        search_results = self._vector_store.search_candidates(
            query_embedding=job_embedding,
            top_k=max(settings.max_match_results, 50),
        )

        ranked = []
        for candidate_id, similarity in search_results:
            candidate = self._candidate_repository.get(candidate_id)
            if candidate is None:
                continue
            ranked.append(
                CandidateMatchResponse(
                    candidateId=candidate.id,
                    similarityScore=similarity,
                    experience=candidate.experience,
                )
            )

        ranked.sort(key=lambda item: (-item.similarityScore, -item.experience))
        top_matches = ranked[: settings.max_match_results]

        return MatchResultsResponse(jobId=job_id, matches=top_matches)
