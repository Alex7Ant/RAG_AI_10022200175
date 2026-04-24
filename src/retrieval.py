# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Dict, List

from src.vector_index import search_index


def _token_set(text: str) -> set:
    return {t.strip(".,:;!?()[]{}\"'").lower() for t in text.split() if t.strip()}


ELECTION_TERMS = {
    "election",
    "electoral",
    "vote",
    "votes",
    "voter",
    "voters",
    "candidate",
    "candidates",
    "party",
    "parties",
    "constituency",
    "constituencies",
    "region",
    "regions",
    "district",
    "districts",
    "poll",
    "polling",
    "results",
    "winner",
    "winners",
    "npp",
    "ndc",
    "cpp",
    "pnc",
    "lpg",
    "gum",
    "gcpp",
    "ndp",
}

BUDGET_TERMS = {
    "budget",
    "fiscal",
    "revenue",
    "tax",
    "taxes",
    "expenditure",
    "expenditures",
    "debt",
    "inflation",
    "economy",
    "economic",
    "policy",
    "policies",
    "sona",
    "address",
    "government",
    "minister",
    "ministry",
}


def _query_domain(query: str) -> str:
    terms = _token_set(query)
    election_hits = terms.intersection(ELECTION_TERMS)
    budget_hits = terms.intersection(BUDGET_TERMS)

    if election_hits and not budget_hits:
        return "election"
    if budget_hits and not election_hits:
        return "budget"
    return "mixed"


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

    domain = _query_domain(query)
    if domain == "election":
        candidate_ids = [i for i, chunk in enumerate(chunks) if chunk.get("source", "").lower().endswith(".csv")]
    elif domain == "budget":
        candidate_ids = [i for i, chunk in enumerate(chunks) if chunk.get("source", "").lower().endswith(".pdf")]
    else:
        candidate_ids = list(range(len(chunks)))

    if not candidate_ids:
        candidate_ids = list(range(len(chunks)))

    candidate_vectors = [index.get("vectors", [])[i] for i in candidate_ids]
    vec_scores, ids = search_index({"vectors": candidate_vectors}, query_vec, top_k=top_k * 3)

    terms = _token_set(query)
    election_hits = terms.intersection(ELECTION_TERMS)
    budget_hits = terms.intersection(BUDGET_TERMS)

    retrieved: List[Dict] = []
    for vec_score, idx in zip(vec_scores, ids):
        if idx < 0 or idx >= len(candidate_ids):
            continue
        chunk_idx = candidate_ids[int(idx)]
        chunk = chunks[chunk_idx]
        kw_score = keyword_overlap_score(query, chunk["text"])

        source_boost = 0.0
        source_path = str(chunk.get("source", "")).lower()
        if source_path.endswith(".csv") and election_hits:
            source_boost = 0.15 if domain == "election" else 0.08
        elif source_path.endswith(".pdf") and budget_hits:
            source_boost = 0.15 if domain == "budget" else 0.08

        final_score = hybrid_alpha * float(vec_score) + (1.0 - hybrid_alpha) * kw_score + source_boost
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