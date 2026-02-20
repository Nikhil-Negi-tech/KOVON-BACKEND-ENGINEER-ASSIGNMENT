"""Dependency wiring for repositories and services."""

from __future__ import annotations

from functools import lru_cache

from app.db.repositories import CandidateRepository, JobRepository
from app.db.vector_store import FaissVectorStore
from app.services.embedding_service import EmbeddingService
from app.services.matching_service import MatchingService


@lru_cache
def get_matching_service() -> MatchingService:
    """Build and cache a singleton matching service instance."""
    candidate_repository = CandidateRepository()
    job_repository = JobRepository()
    vector_store = FaissVectorStore()
    embedding_service = EmbeddingService()

    return MatchingService(
        candidate_repository=candidate_repository,
        job_repository=job_repository,
        vector_store=vector_store,
        embedding_service=embedding_service,
    )
