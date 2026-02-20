"""In-memory repositories for domain entities."""

from __future__ import annotations

from app.models.candidate import Candidate
from app.models.job import Job


class CandidateRepository:
    """Repository for managing candidate records."""

    def __init__(self) -> None:
        self._items: dict[str, Candidate] = {}

    def add(self, candidate: Candidate) -> None:
        """Persist a candidate record."""
        self._items[candidate.id] = candidate

    def get(self, candidate_id: str) -> Candidate | None:
        """Fetch a candidate by ID."""
        return self._items.get(candidate_id)


class JobRepository:
    """Repository for managing job records."""

    def __init__(self) -> None:
        self._items: dict[str, Job] = {}

    def add(self, job: Job) -> None:
        """Persist a job record."""
        self._items[job.id] = job

    def get(self, job_id: str) -> Job | None:
        """Fetch a job by ID."""
        return self._items.get(job_id)
