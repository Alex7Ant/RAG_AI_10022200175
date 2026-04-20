# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.chunking import fixed_token_chunks, sentence_window_chunks
from src.config import load_config
from src.data_sources import load_csv_rows, load_pdf_pages


TEST_QUERIES = [
    "What were election outcomes by region?",
    "What are the major fiscal priorities in the 2025 budget?",
    "Which trends appear in constituency level election data?",
]


def keyword_match(query: str, text: str) -> float:
    q = {t.lower().strip(".,!?") for t in query.split() if t.strip()}
    p = {t.lower().strip(".,!?") for t in text.split() if t.strip()}
    if not q:
        return 0.0
    return len(q.intersection(p)) / len(q)


def evaluate(chunks) -> dict:
    avg_len = sum(len(c["text"]) for c in chunks) / max(1, len(chunks))
    coverage_scores = []
    for q in TEST_QUERIES:
        best = 0.0
        for c in chunks[: min(2000, len(chunks))]:
            score = keyword_match(q, c["text"])
            if score > best:
                best = score
        coverage_scores.append(best)
    return {
        "chunk_count": len(chunks),
        "avg_chunk_characters": avg_len,
        "mean_query_keyword_coverage": sum(coverage_scores) / max(1, len(coverage_scores)),
        "query_scores": dict(zip(TEST_QUERIES, coverage_scores)),
    }


def main() -> None:
    cfg = load_config()
    print("Loading datasets...")
    records = load_csv_rows(cfg.data_csv_path) + load_pdf_pages(cfg.data_pdf_path, max_pages=50)
    print(f"Loaded records: {len(records)}")

    print("Building fixed chunks...")
    fixed_chunks = fixed_token_chunks(records, cfg.chunk_size, cfg.chunk_overlap)
    print(f"Fixed chunks: {len(fixed_chunks)}")
    print("Building sentence chunks...")
    sentence_chunks = sentence_window_chunks(records)
    print(f"Sentence chunks: {len(sentence_chunks)}")

    print("Evaluating fixed strategy...")
    fixed_eval = evaluate(fixed_chunks)
    print("Evaluating sentence strategy...")
    sentence_eval = evaluate(sentence_chunks)

    report = {
        "strategy_fixed": fixed_eval,
        "strategy_sentence": sentence_eval,
        "recommendation": (
            "Choose fixed chunks if precision and local context continuity are better in your manual checks; "
            "choose sentence chunks if interpretability and coherence are better."
        ),
    }

    out_dir = Path("artifacts/experiments")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "part_a_chunking_comparison.json"
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")

    out_md = out_dir / "part_a_chunking_comparison.md"
    out_md.write_text(
        "# Part A Chunking Comparison\n\n"
        f"- Fixed chunk count: {fixed_eval['chunk_count']}\n"
        f"- Fixed mean query coverage: {fixed_eval['mean_query_keyword_coverage']:.4f}\n"
        f"- Sentence chunk count: {sentence_eval['chunk_count']}\n"
        f"- Sentence mean query coverage: {sentence_eval['mean_query_keyword_coverage']:.4f}\n\n"
        "Use this as quantitative evidence and pair it with manual retrieval examples in your log.\n",
        encoding="utf-8",
    )

    print(f"Saved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()