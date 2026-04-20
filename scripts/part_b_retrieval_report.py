# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import load_config
from src.embeddings import Embedder
from src.retrieval import retrieve
from src.vector_index import load_chunks, load_index


QUERIES = [
    "Summarize election outcomes by region.",
    "What fiscal priorities are in the 2025 budget statement?",
    "Tell me how cocoa exports changed in this dataset.",
]


def to_rows(results):
    rows = []
    for r in results:
        rows.append(
            {
                "chunk_id": r["chunk_id"],
                "source": r["source"],
                "vector_score": r["vector_score"],
                "keyword_score": r["keyword_score"],
                "final_score": r["final_score"],
            }
        )
    return rows


def main() -> None:
    cfg = load_config()
    chunks = load_chunks(cfg.chunks_path)
    index = load_index(cfg.index_path)
    embedder = Embedder(cfg.embedding_model)

    report = {
        "part": "B",
        "top_k": cfg.top_k,
        "default_hybrid_alpha": cfg.hybrid_alpha,
        "queries": [],
        "failure_case": {},
    }

    for q in QUERIES:
        default_results = retrieve(index, embedder, chunks, q, top_k=cfg.top_k, hybrid_alpha=cfg.hybrid_alpha)
        tuned_results = retrieve(index, embedder, chunks, q, top_k=cfg.top_k, hybrid_alpha=0.5)
        report["queries"].append(
            {
                "query": q,
                "default": to_rows(default_results),
                "tuned_alpha_0_5": to_rows(tuned_results),
            }
        )

    failure_query = "Tell me how cocoa exports changed in this dataset."
    fail_default = retrieve(index, embedder, chunks, failure_query, top_k=cfg.top_k, hybrid_alpha=cfg.hybrid_alpha)
    fail_tuned = retrieve(index, embedder, chunks, failure_query, top_k=cfg.top_k, hybrid_alpha=0.5)
    report["failure_case"] = {
        "query": failure_query,
        "issue": "Potentially irrelevant retrieval when domain terms are missing from source data.",
        "fix_applied": "Adjusted hybrid_alpha from default to 0.5 to increase lexical influence.",
        "before_top_result": to_rows(fail_default[:1]),
        "after_top_result": to_rows(fail_tuned[:1]),
    }

    out_dir = cfg.experiments_path
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "part_b_retrieval_report.json"
    out_md = out_dir / "part_b_retrieval_report.md"

    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    out_md.write_text(
        "# Part B Retrieval Report\n\n"
        f"- Top-k: {cfg.top_k}\n"
        f"- Default hybrid alpha: {cfg.hybrid_alpha}\n"
        "- Extension used: Query expansion + hybrid scoring.\n"
        "- Failure case included with before/after tuning evidence.\n",
        encoding="utf-8",
    )

    print(f"Saved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()