# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Dict, Iterable, List


def _tokenize(text: str) -> List[str]:
    return text.split()


def _detokenize(tokens: List[str]) -> str:
    return " ".join(tokens)


def fixed_token_chunks(records: Iterable[Dict], chunk_size: int, overlap: int) -> List[Dict]:
    chunks: List[Dict] = []
    chunk_id = 0
    step = max(1, chunk_size - overlap)

    for rec in records:
        tokens = _tokenize(rec["text"])
        for start in range(0, len(tokens), step):
            end = start + chunk_size
            piece = tokens[start:end]
            if not piece:
                continue
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_id}",
                    "doc_id": rec["doc_id"],
                    "source": rec["source"],
                    "text": _detokenize(piece),
                    "meta": {
                        **rec["meta"],
                        "strategy": "fixed",
                        "token_start": start,
                        "token_end": min(end, len(tokens)),
                    },
                }
            )
            chunk_id += 1
    return chunks


def sentence_window_chunks(records: Iterable[Dict], window_sentences: int = 4) -> List[Dict]:
    chunks: List[Dict] = []
    chunk_id = 0

    for rec in records:
        text = rec["text"].replace("?", ".").replace("!", ".")
        sentences = [s.strip() for s in text.split(".") if s.strip()]

        if not sentences:
            continue

        for i in range(0, len(sentences), max(1, window_sentences // 2)):
            group = sentences[i : i + window_sentences]
            if not group:
                continue
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_id}",
                    "doc_id": rec["doc_id"],
                    "source": rec["source"],
                    "text": ". ".join(group) + ".",
                    "meta": {
                        **rec["meta"],
                        "strategy": "sentence",
                        "sentence_start": i,
                        "sentence_end": i + len(group),
                    },
                }
            )
            chunk_id += 1
    return chunks