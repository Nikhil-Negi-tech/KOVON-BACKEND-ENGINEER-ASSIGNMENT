"""Domain model for job entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Job:
    """Represents a job description stored in the system."""

    id: str
    title: str
    country: str
    description: str
