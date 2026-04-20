# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Dict, List

from src.vector_index import search_index


def _token_set(text: str) -> set:
    return {t.strip(".,:;!?()[]{}\"'").lower() for t in text.split() if t.strip()}


def keyword_overlap_score(query: str, passage: str) -> float:
    q = _token_set(query)
    p = _token_set(passage)
    if not q or not p:
        return 0.0
    inter = len(q.intersection(p))
    return inter / max(1, len(q))


def expand_query(query: str) -> str:
    expansions = {
        "election": ["vote", "poll", "constituency"],
        "budget": ["fiscal", "expenditure", "revenue"],
        "gdp": ["growth", "economy"],
        "inflation": ["price", "cpi"],
        "education": ["school", "student", "training"],
    }
    terms = _token_set(query)
    extra: List[str] = []
    for t in terms:
        if t in expansions:
            extra.extend(expansions[t])
    return query if not extra else f"{query} {' '.join(extra)}"


def retrieve(
    index,
    embedder,
    chunks: List[Dict],
    query: str,
    top_k: int,
    hybrid_alpha: float,
) -> List[Dict]:
    expanded = expand_query(query)
    query_vec = embedder.encode([expanded])

    vec_scores, ids = search_index(index, query_vec, top_k=top_k * 3)

    retrieved: List[Dict] = []
    for vec_score, idx in zip(vec_scores, ids):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[int(idx)]
        kw_score = keyword_overlap_score(query, chunk["text"])
        final_score = hybrid_alpha * float(vec_score) + (1.0 - hybrid_alpha) * kw_score
        retrieved.append(
            {
                **chunk,
                "vector_score": float(vec_score),
                "keyword_score": float(kw_score),
                "final_score": float(final_score),
            }
        )

    retrieved.sort(key=lambda x: x["final_score"], reverse=True)
    return retrieved[:top_k]