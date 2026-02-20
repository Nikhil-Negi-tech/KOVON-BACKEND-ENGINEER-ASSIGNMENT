from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Semantic Candidate Matching API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    max_match_results: int = int(os.getenv("MAX_MATCH_RESULTS", "5"))


settings = Settings()
