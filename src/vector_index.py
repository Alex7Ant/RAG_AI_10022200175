# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _cosine(a: List[float], b: List[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den_a = math.sqrt(sum(x * x for x in a)) or 1.0
    den_b = math.sqrt(sum(y * y for y in b)) or 1.0
    return num / (den_a * den_b)


def build_faiss_index(vectors: List[List[float]]) -> Dict[str, Any]:
    # Name kept for API compatibility with earlier code.
    return {"vectors": vectors, "size": len(vectors)}


def save_index(index: Dict[str, Any], index_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", encoding="utf-8") as f:
        json.dump(index, f)


def load_index(index_path: Path) -> Dict[str, Any]:
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")
    with index_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_chunks(chunks: List[Dict], chunks_path: Path) -> None:
    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    with chunks_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_chunks(chunks_path: Path) -> List[Dict]:
    if not chunks_path.exists():
        raise FileNotFoundError(f"Chunks file not found: {chunks_path}")
    rows: List[Dict] = []
    with chunks_path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def search_index(index: Dict[str, Any], query_vec: List[List[float]], top_k: int) -> Tuple[List[float], List[int]]:
    q = query_vec[0]
    vectors = index.get("vectors", [])
    scored = [(i, _cosine(q, v)) for i, v in enumerate(vectors)]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_k]
    return [s for _, s in top], [i for i, _ in top]