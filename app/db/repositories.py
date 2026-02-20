from __future__ import annotations

from app.models.candidate import Candidate
from app.models.job import Job


class CandidateRepository:
    def __init__(self) -> None:
        self._items: dict[str, Candidate] = {}

    def add(self, candidate: Candidate) -> None:
        self._items[candidate.id] = candidate

    def get(self, candidate_id: str) -> Candidate | None:
        return self._items.get(candidate_id)


class JobRepository:
    def __init__(self) -> None:
        self._items: dict[str, Job] = {}

    def add(self, job: Job) -> None:
        self._items[job.id] = job

    def get(self, job_id: str) -> Job | None:
        return self._items.get(job_id)
