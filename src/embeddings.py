# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import List

import math
import re
import hashlib
import os


class Embedder:
    def __init__(self, model_name: str, fallback_dim: int = 256):
        self.model_name = model_name
        self.fallback_dim = fallback_dim
        self.model = None
        enable_st = os.getenv("ENABLE_ST_EMBEDDINGS", "0").strip() == "1"
        if enable_st:
            try:
                from sentence_transformers import SentenceTransformer

                self.model = SentenceTransformer(model_name)
            except Exception:
                self.model = None

    def _hash_embed(self, text: str) -> List[float]:
        vec = [0.0] * self.fallback_dim
        tokens = re.findall(r"[A-Za-z0-9_]+", text.lower())
        if not tokens:
            return vec

        for t in tokens:
            digest = hashlib.md5(t.encode("utf-8")).hexdigest()
            idx = int(digest[:8], 16) % self.fallback_dim
            vec[idx] += 1.0

        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def encode(self, texts: List[str]) -> List[List[float]]:
        if self.model is not None:
            vectors = self.model.encode(texts, normalize_embeddings=True)
            return [list(map(float, row)) for row in vectors]
        return [self._hash_embed(t) for t in texts]