# Student Name: Alexandre Anthony
# Student Index: 10022200175

from typing import Optional

import requests
from openai import OpenAI


def _fallback_answer(prompt: str) -> str:
    marker = "Retrieved Context:\n"
    context = ""
    if marker in prompt:
        context = prompt.split(marker, 1)[1]
    context = context.strip()
    if not context:
        return "I could not find this in the retrieved context."

    lines = [line.strip() for line in context.splitlines() if line.strip()]
    picked = []
    for line in lines:
        if line.startswith("[") and "source=" in line:
            continue
        picked.append(line)
        if len(picked) == 2:
            break

    if not picked:
        return "I could not find this in the retrieved context."
    return (
        "Direct answer: " + " ".join(picked)[:600] + "\n"
        "Evidence citations: [1]\n"
        "Uncertainty note: Generated with fallback mode because LLM endpoint was unavailable."
    )


def ask_llm(
    provider: str,
    prompt: str,
    openai_api_key: str,
    openai_model: str,
    ollama_base_url: str,
    ollama_model: str,
    temperature: float = 0.1,
) -> str:
    provider = provider.lower().strip()

    if provider == "openai":
        if not openai_api_key:
            return _fallback_answer(prompt)
        try:
            client = OpenAI(api_key=openai_api_key)
            resp = client.chat.completions.create(
                model=openai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            return _fallback_answer(prompt)

    if provider == "ollama":
        try:
            url = f"{ollama_base_url.rstrip('/')}/api/chat"
            payload = {
                "model": ollama_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperature},
            }
            r = requests.post(url, json=payload, timeout=3)
            r.raise_for_status()
            data = r.json()
            return (data.get("message") or {}).get("content", "")
        except Exception:
            return _fallback_answer(prompt)

    raise ValueError("LLM provider must be 'openai' or 'ollama'.")