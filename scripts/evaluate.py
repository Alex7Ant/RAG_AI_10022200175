# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import load_config
from src.llm_client import ask_llm
from src.pipeline import answer_query


def answer_without_retrieval(query: str) -> str:
    cfg = load_config()
    prompt = (
        "Answer the question directly without any retrieved context. "
        "If uncertain, still provide your best answer.\n\n"
        f"Question: {query}"
    )
    return ask_llm(
        provider=cfg.llm_provider,
        prompt=prompt,
        openai_api_key=cfg.openai_api_key,
        openai_model=cfg.openai_model,
        ollama_base_url=cfg.ollama_base_url,
        ollama_model=cfg.ollama_model,
        temperature=0.2,
    )


def main() -> None:
    cfg = load_config()
    queries = [
        "Summarize election trends in northern regions and cite evidence.",
        "Which exact section in the 2025 budget proposes reducing VAT to 10%?",
    ]

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "results": [],
    }

    for q in queries:
        rag = answer_query(q)
        base = answer_without_retrieval(q)
        report["results"].append(
            {
                "query": q,
                "rag_answer": rag["answer"],
                "rag_top_chunks": [
                    {
                        "chunk_id": r["chunk_id"],
                        "source": r["source"],
                        "score": r["final_score"],
                    }
                    for r in rag["retrieved"]
                ],
                "baseline_answer": base,
            }
        )

    cfg.experiments_path.mkdir(parents=True, exist_ok=True)
    out = cfg.experiments_path / "adversarial_eval.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved evaluation report to: {out}")


if __name__ == "__main__":
    main()