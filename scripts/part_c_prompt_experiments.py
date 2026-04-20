# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import load_config
from src.embeddings import Embedder
from src.llm_client import ask_llm
from src.prompting import build_prompt, select_context
from src.retrieval import retrieve
from src.vector_index import load_chunks, load_index


def main() -> None:
    cfg = load_config()
    chunks = load_chunks(cfg.chunks_path)
    index = load_index(cfg.index_path)
    embedder = Embedder(cfg.embedding_model)

    query = "What are the key priorities in the 2025 Budget Statement?"
    retrieved = retrieve(index, embedder, chunks, query, top_k=cfg.top_k, hybrid_alpha=cfg.hybrid_alpha)
    context_text, selected = select_context(retrieved)

    prompt_v1 = (
        "Answer the question using the context below.\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context_text}\n"
    )
    prompt_v2 = build_prompt(query, context_text)

    answer_v1 = ask_llm(
        provider=cfg.llm_provider,
        prompt=prompt_v1,
        openai_api_key=cfg.openai_api_key,
        openai_model=cfg.openai_model,
        ollama_base_url=cfg.ollama_base_url,
        ollama_model=cfg.ollama_model,
        temperature=0.2,
    )
    answer_v2 = ask_llm(
        provider=cfg.llm_provider,
        prompt=prompt_v2,
        openai_api_key=cfg.openai_api_key,
        openai_model=cfg.openai_model,
        ollama_base_url=cfg.ollama_base_url,
        ollama_model=cfg.ollama_model,
        temperature=0.1,
    )

    report = {
        "part": "C",
        "query": query,
        "selected_chunks": [c["chunk_id"] for c in selected],
        "prompt_v1": prompt_v1,
        "prompt_v2": prompt_v2,
        "answer_v1": answer_v1,
        "answer_v2": answer_v2,
        "analysis": {
            "expected_improvement": "Prompt v2 should reduce hallucination and increase citation behavior.",
            "context_control": "Applied context selection with max characters before prompt construction.",
        },
    }

    out_dir = cfg.experiments_path
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "part_c_prompt_experiments.json"
    out_md = out_dir / "part_c_prompt_experiments.md"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(
        "# Part C Prompt Engineering Report\n\n"
        "- Same query tested with two prompt templates.\n"
        "- Prompt v2 enforces grounding and citation structure.\n"
        "- Output differences are stored in the JSON report.\n",
        encoding="utf-8",
    )

    print(f"Saved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()