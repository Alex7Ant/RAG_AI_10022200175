# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Dict, List, Tuple


def select_context(chunks: List[Dict], max_chars: int = 4500) -> Tuple[str, List[Dict]]:
    selected: List[Dict] = []
    used = 0
    for chunk in chunks:
        text = chunk["text"]
        if used + len(text) > max_chars:
            break
        selected.append(chunk)
        used += len(text)

    lines = []
    for i, c in enumerate(selected, start=1):
        source = c.get("source", "unknown")
        page = c.get("meta", {}).get("page")
        page_info = f", page={page}" if page else ""
        lines.append(f"[{i}] source={source}{page_info}\n{c['text']}")

    return "\n\n".join(lines), selected


def build_prompt(user_query: str, context_text: str) -> str:
    return (
        "You are an Academic City AI assistant.\n"
        "Use only the provided context to answer.\n"
        "If the answer is not in context, say: 'I could not find this in the retrieved context.'\n"
        "Avoid repeating the same sentences or paragraphs from the context verbatim; instead, synthesize and paraphrase.\n"
        "Keep answers concise and directly address the user query.\n"
        "Cite supporting chunks using [1], [2], etc.\n"
        "\n"
        f"User Question:\n{user_query}\n\n"
        f"Retrieved Context:\n{context_text}\n\n"
        "Answer format:\n"
        "1) Direct answer (1-4 sentences)\n"
        "2) Evidence citations\n"
        "3) Uncertainty note (if applicable)\n"
    )