# backend/app/semantic_matcher.py
import os
import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Tuple

VECTOR_DIR = os.path.join(os.path.dirname(__file__), "vector_store")
os.makedirs(VECTOR_DIR, exist_ok=True)

# Choose a small, fast model for CPU-friendly inference
MODEL_NAME = "all-MiniLM-L6-v2"

# Load model once (module import)
MODEL = SentenceTransformer(MODEL_NAME)


def _text_hash(text: str) -> str:
    """Stable short hash for a text blob."""
    h = hashlib.sha256()
    h.update((text or "").encode("utf-8"))
    return h.hexdigest()


def _vector_path(text_hash: str) -> str:
    return os.path.join(VECTOR_DIR, f"{text_hash}.npy")


def get_embedding(text: str) -> np.ndarray:
    """
    Get embedding for text. Uses on-disk cache to avoid recomputation.
    Returns a numpy vector.
    """
    text = (text or "").strip()
    if not text:
        # return zero vector
        return np.zeros(MODEL.get_sentence_embedding_dimension(), dtype=np.float32)

    h = _text_hash(text)
    path = _vector_path(h)
    if os.path.exists(path):
        try:
            vec = np.load(path)
            return vec
        except Exception:
            # fallback to recompute if load fails
            pass

    emb = MODEL.encode([text], convert_to_numpy=True)[0]
    # save cache
    try:
        np.save(path, emb)
    except Exception:
        # ignore cache write errors
        pass
    return emb


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity in [-1,1]. Returns float."""
    if a is None or b is None:
        return 0.0
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def semantic_score_percent(text1: str, text2: str) -> float:
    """
    Returns a semantic similarity percent in range [0,100].
    Uses Sentence-Transformers + cached embeddings.
    """
    v1 = get_embedding(text1)
    v2 = get_embedding(text2)
    sim = cosine_similarity(v1, v2)  # [-1,1]
    # map [-1,1] to [0,1], then to percentage
    scaled = max(-1.0, min(1.0, sim))
    normalized = (scaled + 1.0) / 2.0
    return round(normalized * 100.0, 2)

"""
Loads all-MiniLM-L6-v2 once (lightweight, CPU friendly).

Caches embeddings as .npy files in backend/app/vector_store/ using SHA-256 hash of text — very simple and effective.

Exposes semantic_score_percent(text1, text2) that returns a 0–100 semantic similarity.
"""