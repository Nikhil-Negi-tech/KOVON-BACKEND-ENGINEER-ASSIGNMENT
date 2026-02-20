"""Domain model for candidate entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Candidate:
    """Represents a candidate profile stored in the system."""

    id: str
    name: str
    skill_description: str
    experience: int
    location: str
