"""Embedding generation service."""

from __future__ import annotations

import asyncio

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    """Creates dense text embeddings using a HuggingFace sentence-transformer model."""

    def __init__(self, model_name: str = settings.embedding_model_name) -> None:
        self._model = SentenceTransformer(model_name)
        self._dimension = self._model.get_sentence_embedding_dimension()

    @property
    def dimension(self) -> int:
        """Return embedding vector dimension."""
        return int(self._dimension)

    async def embed_text(self, text: str) -> np.ndarray:
        """Asynchronously embed a single input string."""

        def _encode() -> np.ndarray:
            vector = self._model.encode(text, normalize_embeddings=False)
            return np.asarray(vector, dtype="float32")

        return await asyncio.to_thread(_encode)
