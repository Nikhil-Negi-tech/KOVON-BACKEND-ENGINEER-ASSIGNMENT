from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Candidate:
    id: str
    name: str
    skill_description: str
    experience: int
    location: str
