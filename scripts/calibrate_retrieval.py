import json
from pathlib import Path
from itertools import product
from src.vector_index import load_index, load_chunks
from src.embeddings import Embedder
from src.retrieval import retrieve


def evaluate(params, index, chunks, embedder, queries):
    hybrid_alpha, primary, secondary = params
    correct = 0
    total = 0
    sb = {"primary": primary, "secondary": secondary}
    for q, expected in queries:
        res = retrieve(index, embedder, chunks, q, top_k=1, hybrid_alpha=hybrid_alpha, source_boosts=sb)
        top = res[0] if res else None
        total += 1
        if not top:
            continue
        src = str(top.get("source", "")).lower()
        if expected == "csv" and src.endswith(".csv"):
            correct += 1
        if expected == "pdf" and src.endswith(".pdf"):
            correct += 1

    return correct / max(1, total)


if __name__ == '__main__':
    index = load_index(Path("artifacts/index.faiss"))
    chunks = load_chunks(Path("artifacts/chunks.jsonl"))
    embedder = Embedder("all-MiniLM-L6-v2")

    # expanded sample queries for calibration (diverse queries to better tune routing)
    queries = [
        ("Who won the 2020 parliamentary election in the Accra Central constituency?", "csv"),
        ("Who was the NPP candidate in Accra Central in 2020?", "csv"),
        ("List the votes for NPP candidates in 2020 in Greater Accra.", "csv"),
        ("Which party gained the most seats in 2020?", "csv"),
        ("Show votes percent for Nana Akufo Addo in 2020.", "csv"),
        ("What is the breakdown of votes by constituency for 2020 in Central Region?", "csv"),
        ("What is the government's projected revenue for the 2025 financial year?", "pdf"),
        ("Summarize the fiscal deficit projection for 2025.", "pdf"),
        ("How much is allocated to education in the 2025 budget?", "pdf"),
        ("What are the headline tax policy changes announced in the 2025 budget?", "pdf"),
        ("Provide the budget allocation for health for 2025.", "pdf"),
        ("What is the Minister's statement on inflation in the 2025 budget?", "pdf"),
        ("Who is listed as the Minister for Finance in the 2025 Budget Statement?", "pdf"),
        ("Which constituencies are in Greater Accra Region?", "mixed"),
    ]

    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    primaries = [0.05, 0.1, 0.15, 0.2]
    secondaries = [0.0, 0.04, 0.08, 0.12]

    results = []
    for params in product(alphas, primaries, secondaries):
        score = evaluate(params, index, chunks, embedder, queries)
        results.append((params, score))

    results.sort(key=lambda x: x[1], reverse=True)

    best_params, best_score = results[0]
    output = {
        "best": {"hybrid_alpha": best_params[0], "primary": best_params[1], "secondary": best_params[2], "score": best_score},
        "all": [
            {"hybrid_alpha": p[0], "primary": p[1], "secondary": p[2], "score": s} for (p, s) in results
        ],
    }

    out_path = Path("artifacts/experiments/retrieval_tuning.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2))
    print(f"Wrote tuning results to {out_path}")
    print("Best:", output["best"])
