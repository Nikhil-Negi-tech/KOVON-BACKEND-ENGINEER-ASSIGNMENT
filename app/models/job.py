from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Job:
    id: str
    title: str
    country: str
    description: str
