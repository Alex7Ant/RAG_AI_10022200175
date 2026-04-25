from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from src.vector_index import load_index, load_chunks
from src.embeddings import Embedder
from src.retrieval import retrieve
from src.prompting import select_context, build_prompt
from src.llm_client import ask_llm
from src.config import load_config
import json
from pathlib import Path


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


app = FastAPI(title="RAG API")


@app.on_event("startup")
def startup():
    global CONFIG, INDEX, CHUNKS, EMBEDDER
    CONFIG = load_config()
    INDEX = load_index(Path(CONFIG.index_path))
    CHUNKS = load_chunks(Path(CONFIG.chunks_path))
    EMBEDDER = Embedder(CONFIG.embedding_model)


@app.post("/query")
def query(req: QueryRequest):
    domain = None
    # attempt to load tuning results and pass source_boosts
    tuning_path = Path(CONFIG.experiments_path) / "retrieval_tuning.json"
    source_boosts = None
    try:
        if tuning_path.exists():
            data = json.loads(tuning_path.read_text(encoding="utf-8"))
            best = data.get("best", {})
            # map primary/secondary to floats
            source_boosts = {"primary": float(best.get("primary", 0.15)), "secondary": float(best.get("secondary", 0.08))}
    except Exception:
        source_boosts = None

    retrieved = retrieve(INDEX, EMBEDDER, CHUNKS, req.query, top_k=req.top_k, hybrid_alpha=CONFIG.hybrid_alpha, source_boosts=source_boosts)
    context_text, selected = select_context(retrieved, max_chars=3500)
    prompt = build_prompt(req.query, context_text)
    answer = ask_llm(
        CONFIG.llm_provider,
        prompt,
        CONFIG.openai_api_key,
        CONFIG.openai_model,
        CONFIG.ollama_base_url,
        CONFIG.ollama_model,
    )
    return {"answer": answer, "retrieved": selected}
