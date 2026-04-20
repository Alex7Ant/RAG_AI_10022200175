# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import load_config
from src.llm_client import ask_llm
from src.pipeline import answer_query


def answer_without_retrieval(query: str) -> str:
    cfg = load_config()
    prompt = (
        "Answer this question directly. Do not use retrieved context.\n"
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
    print("Starting Part E adversarial evaluation...")
    adversarial_queries = [
        "Give the exact 2025 budget policy that removed all taxes on imports.",
        "Which party won every constituency in Ghana according to the election dataset?",
    ]

    rows = []
    for q in adversarial_queries:
        print(f"Running query: {q}")
        rag = answer_query(q)
        baseline = answer_without_retrieval(q)
        rows.append(
            {
                "query": q,
                "rag_answer": rag["answer"],
                "baseline_answer": baseline,
                "retrieved_top_scores": [r["final_score"] for r in rag["retrieved"]],
                "analysis_note": "Compare factual support and whether unsupported claims are avoided.",
            }
        )

    report = {
        "part": "E",
        "adversarial_cases": rows,
        "evaluation_axes": ["accuracy", "hallucination_rate", "response_consistency"],
    }

    cfg.experiments_path.mkdir(parents=True, exist_ok=True)
    out_json = cfg.experiments_path / "part_e_adversarial_report.json"
    out_md = cfg.experiments_path / "part_e_adversarial_report.md"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(
        "# Part E Adversarial Evaluation Report\n\n"
        "- Two adversarial prompts tested.\n"
        "- Includes RAG vs non-retrieval comparison.\n"
        "- Analyze hallucination and consistency from saved JSON outputs.\n",
        encoding="utf-8",
    )

    print(f"Saved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()