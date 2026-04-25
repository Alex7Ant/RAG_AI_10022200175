from pathlib import Path
from src.vector_index import load_index, load_chunks
from src.embeddings import Embedder
from src.retrieval import retrieve


def run_test(query):
    index = load_index(Path("artifacts/index.faiss"))
    chunks = load_chunks(Path("artifacts/chunks.jsonl"))
    embedder = Embedder("all-MiniLM-L6-v2")
    results = retrieve(index, embedder, chunks, query, top_k=5, hybrid_alpha=0.75)
    print(f"\nQuery: {query}")
    for i, r in enumerate(results, 1):
        print(f"{i}. source={r.get('source')} final_score={r.get('final_score'):.4f} vector_score={r.get('vector_score'):.4f} keyword_score={r.get('keyword_score'):.4f}")
        text = r.get("text", "")
        snippet = text.replace('\n',' ')[:300]
        print(f"   snippet: {snippet}\n")


if __name__ == '__main__':
    run_test("Who won the 2020 parliamentary election in the Accra Central constituency?")
    run_test("What is the government's projected revenue for the 2025 financial year?")
