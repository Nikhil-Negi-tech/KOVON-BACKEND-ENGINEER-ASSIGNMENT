"""FAISS-based vector storage and search utilities."""

from __future__ import annotations

import importlib
from typing import Any

import numpy as np


class FaissVectorStore:
    """Stores candidate and job embeddings and performs cosine similarity search."""

    def __init__(self) -> None:
        self._dimension: int | None = None
        self._candidate_index: Any | None = None
        self._job_index: Any | None = None

        self._candidate_ids: list[str] = []
        self._job_ids: list[str] = []

        self._job_embeddings: dict[str, np.ndarray] = {}

    def _ensure_indexes(self, dimension: int) -> None:
        """Create FAISS indexes lazily using the first observed dimension."""
        try:
            faiss = importlib.import_module("faiss")
        except ImportError as error:  # pragma: no cover
            raise ImportError("faiss-cpu must be installed to use vector storage.") from error

        if self._dimension is None:
            self._dimension = dimension
            self._candidate_index = faiss.IndexFlatIP(dimension)
            self._job_index = faiss.IndexFlatIP(dimension)
            return

        if self._dimension != dimension:
            raise ValueError(
                f"Embedding dimension mismatch. Expected {self._dimension}, got {dimension}."
            )

    @staticmethod
    def _normalize(embedding: np.ndarray) -> np.ndarray:
        """Return an L2-normalized embedding suitable for cosine similarity with inner product."""
        vector = embedding.astype("float32").reshape(1, -1)
        norm = np.linalg.norm(vector, axis=1, keepdims=True)
        norm[norm == 0.0] = 1.0
        return vector / norm

    def add_candidate(self, candidate_id: str, embedding: np.ndarray) -> None:
        """Store a candidate embedding in the FAISS index."""
        self._ensure_indexes(embedding.shape[0])
        normalized = self._normalize(embedding)
        assert self._candidate_index is not None

        self._candidate_index.add(normalized)
        self._candidate_ids.append(candidate_id)

    def add_job(self, job_id: str, embedding: np.ndarray) -> None:
        """Store a job embedding in FAISS and in lookup cache for direct retrieval."""
        self._ensure_indexes(embedding.shape[0])
        normalized = self._normalize(embedding)
        assert self._job_index is not None

        self._job_index.add(normalized)
        self._job_ids.append(job_id)
        self._job_embeddings[job_id] = embedding.astype("float32")

    def get_job_embedding(self, job_id: str) -> np.ndarray | None:
        """Fetch raw job embedding from cache by job ID."""
        return self._job_embeddings.get(job_id)

    def search_candidates(self, query_embedding: np.ndarray, top_k: int) -> list[tuple[str, float]]:
        """Search candidate embeddings and return candidate IDs with cosine similarity scores."""
        if not self._candidate_ids or self._candidate_index is None:
            return []

        normalized_query = self._normalize(query_embedding)
        candidate_count = len(self._candidate_ids)
        k = min(top_k, candidate_count)

        distances, indices = self._candidate_index.search(normalized_query, k)
        results: list[tuple[str, float]] = []

        for score, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            candidate_id = self._candidate_ids[idx]
            results.append((candidate_id, float(score)))

        return results
