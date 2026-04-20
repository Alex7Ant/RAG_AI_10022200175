# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Dict

from src.config import load_config
from src.embeddings import Embedder
from src.llm_client import ask_llm
from src.logging_utils import log_event
from src.prompting import build_prompt, select_context
from src.retrieval import retrieve
from src.vector_index import load_chunks, load_index


def answer_query(user_query: str) -> Dict:
    cfg = load_config()

    chunks = load_chunks(cfg.chunks_path)
    index = load_index(cfg.index_path)
    embedder = Embedder(cfg.embedding_model)

    log_event(cfg.logs_path, "query_received", {"query": user_query})

    retrieved = retrieve(
        index=index,
        embedder=embedder,
        chunks=chunks,
        query=user_query,
        top_k=cfg.top_k,
        hybrid_alpha=cfg.hybrid_alpha,
    )
    log_event(
        cfg.logs_path,
        "retrieval",
        {
            "top_k": cfg.top_k,
            "results": [
                {
                    "chunk_id": r["chunk_id"],
                    "source": r["source"],
                    "vector_score": r["vector_score"],
                    "keyword_score": r["keyword_score"],
                    "final_score": r["final_score"],
                }
                for r in retrieved
            ],
        },
    )

    context_text, selected = select_context(retrieved)
    log_event(
        cfg.logs_path,
        "context_selection",
        {
            "selected_chunks": [c["chunk_id"] for c in selected],
            "context_characters": len(context_text),
        },
    )

    prompt = build_prompt(user_query, context_text)
    log_event(cfg.logs_path, "prompt", {"prompt": prompt})

    response = ask_llm(
        provider=cfg.llm_provider,
        prompt=prompt,
        openai_api_key=cfg.openai_api_key,
        openai_model=cfg.openai_model,
        ollama_base_url=cfg.ollama_base_url,
        ollama_model=cfg.ollama_model,
    )
    log_event(cfg.logs_path, "response", {"answer": response})

    return {
        "query": user_query,
        "retrieved": retrieved,
        "selected_context": selected,
        "prompt": prompt,
        "answer": response,
    }