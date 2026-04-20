# Student Name: Alexandre Anthony
# Student Index: 10022200175

import argparse
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.chunking import fixed_token_chunks, sentence_window_chunks
from src.config import load_config
from src.data_sources import load_csv_rows, load_pdf_pages
from src.embeddings import Embedder
from src.vector_index import build_faiss_index, save_chunks, save_index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", choices=["fixed", "sentence"], default="fixed")
    args = parser.parse_args()

    cfg = load_config()

    print("Loading CSV and PDF records...")
    csv_records = load_csv_rows(cfg.data_csv_path)
    pdf_records = load_pdf_pages(cfg.data_pdf_path, max_pages=50)
    records = csv_records + pdf_records
    print(f"Records loaded: {len(records)}")

    if args.strategy == "fixed":
        print("Building fixed chunks...")
        chunks = fixed_token_chunks(records, cfg.chunk_size, cfg.chunk_overlap)
    else:
        print("Building sentence chunks...")
        chunks = sentence_window_chunks(records)
    print(f"Chunks created: {len(chunks)}")

    embedder = Embedder(cfg.embedding_model)
    print("Encoding chunks...")
    vectors = embedder.encode([c["text"] for c in chunks])
    print("Building and saving index...")
    index = build_faiss_index(vectors)

    save_chunks(chunks, cfg.chunks_path)
    save_index(index, cfg.index_path)

    cfg.experiments_path.mkdir(parents=True, exist_ok=True)
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strategy": args.strategy,
        "chunk_count": len(chunks),
        "avg_chunk_chars": sum(len(c["text"]) for c in chunks) / max(1, len(chunks)),
        "chunk_size": cfg.chunk_size,
        "chunk_overlap": cfg.chunk_overlap,
    }
    out_path = cfg.experiments_path / f"ingest_summary_{args.strategy}.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Ingestion complete")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()