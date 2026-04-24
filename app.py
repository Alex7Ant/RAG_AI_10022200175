# Student Name: Alexandre Anthony
# Student Index: 10022200175

from datetime import datetime
from uuid import uuid4

import streamlit as st

from src.pipeline import answer_query


st.set_page_config(page_title="Academic City Manual RAG", page_icon="💬", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #f6f3ec;
    --panel: #ffffff;
    --panel-soft: rgba(255, 255, 255, 0.74);
    --ink: #18202a;
    --muted: #5a6675;
    --line: rgba(24, 32, 42, 0.10);
    --brand: #0f6a62;
    --brand-strong: #0a534d;
    --accent: #e58f2a;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(229, 143, 42, 0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(15, 106, 98, 0.14), transparent 26%),
        linear-gradient(180deg, #fbf7ef 0%, #eef2f7 100%);
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--ink);
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.02em;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(17, 26, 37, 0.98), rgba(27, 38, 52, 0.98));
    color: #edf2f7;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] * {
    color: inherit;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.08);
    color: #f7fafc;
    border-radius: 12px;
    padding: 0.55rem 0.8rem;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.14);
}

.sidebar-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin-top: 0.2rem;
    margin-bottom: 0.2rem;
}

.sidebar-subtitle {
    color: rgba(237, 242, 247, 0.78);
    font-size: 0.92rem;
    line-height: 1.35;
    margin-bottom: 1rem;
}

.chat-shell {
    max-width: 1100px;
    margin: 0 auto;
}

.chat-header {
    background: linear-gradient(120deg, rgba(15, 106, 98, 0.97), rgba(25, 84, 138, 0.92));
    color: #fff;
    border-radius: 22px;
    padding: 1rem 1.2rem;
    box-shadow: 0 18px 36px rgba(18, 32, 48, 0.18);
    margin-bottom: 1rem;
}

.chat-header h1 {
    margin: 0;
    font-size: 1.8rem;
}

.chat-header p {
    margin: 0.35rem 0 0 0;
    opacity: 0.95;
}

.chat-transcript {
    padding-top: 0.25rem;
    padding-bottom: 0.75rem;
}

.message {
    border: 1px solid var(--line);
    background: var(--panel-soft);
    border-radius: 18px;
    padding: 0.95rem 1rem;
    box-shadow: 0 10px 24px rgba(26, 36, 49, 0.05);
    margin-bottom: 0.9rem;
    backdrop-filter: blur(4px);
}

.message-user {
    border-left: 4px solid var(--accent);
}

.message-assistant {
    border-left: 4px solid var(--brand);
}

.message-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 0.45rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.message-content {
    white-space: pre-wrap;
    line-height: 1.55;
}

.block-card {
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.82);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    box-shadow: 0 10px 24px rgba(30, 36, 48, 0.08);
    margin-bottom: 0.75rem;
}

.score-line {
    color: var(--muted);
    font-size: 0.92rem;
}

.small-label {
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.35rem;
}

[data-testid="stChatInput"] {
    border-top: 1px solid rgba(24, 32, 42, 0.08);
    padding-top: 0.5rem;
}

[data-testid="stChatInput"] textarea {
    border-radius: 16px !important;
}

[data-testid="stExpander"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.7);
}
</style>
    """,
    unsafe_allow_html=True,
)


def _init_state() -> None:
    if "chats" not in st.session_state:
        chat_id = str(uuid4())
        st.session_state.chats = {
            chat_id: {
                "id": chat_id,
                "title": "New chat",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "messages": [],
            }
        }
        st.session_state.chat_order = [chat_id]
        st.session_state.current_chat_id = chat_id


def _new_chat() -> None:
    chat_id = str(uuid4())
    st.session_state.chats[chat_id] = {
        "id": chat_id,
        "title": "New chat",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "messages": [],
    }
    st.session_state.chat_order.insert(0, chat_id)
    st.session_state.current_chat_id = chat_id


def _get_current_chat() -> dict:
    return st.session_state.chats[st.session_state.current_chat_id]


def _chat_title(chat: dict) -> str:
    if chat.get("title") and chat["title"] != "New chat":
        return chat["title"]
    for message in chat.get("messages", []):
        if message["role"] == "user" and message["content"].strip():
            text = message["content"].strip().replace("\n", " ")
            return text[:42] + ("..." if len(text) > 42 else "")
    return "New chat"


_init_state()
current_chat = _get_current_chat()

with st.sidebar:
    st.markdown('<div class="sidebar-title">Academic City RAG</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtitle">ChatGPT-style workspace for testing the manual RAG pipeline, browsing recent chats, and starting a clean conversation.</div>',
        unsafe_allow_html=True,
    )
    if st.button("+ New chat", use_container_width=True):
        _new_chat()
        st.rerun()

    st.markdown("### Recent chats")
    recent_ids = st.session_state.chat_order[:8]
    for chat_id in recent_ids:
        chat = st.session_state.chats[chat_id]
        label = _chat_title(chat)
        prefix = "• " if chat_id == st.session_state.current_chat_id else "  "
        if st.button(f"{prefix}{label}", key=f"chat_{chat_id}", use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

    st.markdown("### Settings")
    st.caption("The assistant answers from the configured LLM backend and the local document index.")

st.markdown(
    '<div class="chat-shell">',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="chat-header">
  <h1>Academic City Manual RAG Assistant</h1>
  <p>Ask about the election dataset, the 2025 budget, or cross-document comparisons. Use the sidebar to switch or start chats.</p>
</div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="chat-transcript">', unsafe_allow_html=True)

for message in current_chat["messages"]:
    role = message["role"]
    if role == "user":
        st.markdown(
            f'<div class="message message-user"><div class="message-meta">You</div><div class="message-content">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="message message-assistant"><div class="message-meta">Assistant</div><div class="message-content">{message["content"]}</div></div>',
            unsafe_allow_html=True,
        )
        if message.get("result"):
            result = message["result"]
            cols = st.columns([2.15, 1])
            with cols[0]:
                st.markdown('<div class="small-label">Retrieved evidence</div>', unsafe_allow_html=True)
                for i, r in enumerate(result["retrieved"], start=1):
                    st.markdown(
                        "<div class='block-card'>"
                        f"<h4>{i}. {r['chunk_id']}</h4>"
                        f"<div class='score-line'>score={r['final_score']:.4f} "
                        f"(vector={r['vector_score']:.4f}, keyword={r['keyword_score']:.4f})</div>"
                        f"<div class='score-line'>source: {r['source']}</div>"
                        f"<p>{r['text']}</p>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
            with cols[1]:
                st.markdown('<div class="small-label">Run snapshot</div>', unsafe_allow_html=True)
                st.markdown(
                    "<div class='block-card'>"
                    f"<div><strong>Retrieved Chunks:</strong> {len(result['retrieved'])}</div>"
                    f"<div><strong>Context Chunks:</strong> {len(result['selected_context'])}</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                with st.expander("Prompt sent to LLM"):
                    st.code(result["prompt"])
                with st.expander("Selected context chunks"):
                    for c in result["selected_context"]:
                        st.write(f"- {c['chunk_id']}")

st.markdown('</div>', unsafe_allow_html=True)

prompt = st.chat_input("Message Academic City Manual RAG")
if prompt and prompt.strip():
    user_message = prompt.strip()
    current_chat["messages"].append({"role": "user", "content": user_message})
    if current_chat["title"] == "New chat":
        current_chat["title"] = user_message[:42] + ("..." if len(user_message) > 42 else "")

    with st.spinner("Running retrieval and generation..."):
        result = answer_query(user_message)

    assistant_text = result["answer"]
    current_chat["messages"].append(
        {
            "role": "assistant",
            "content": assistant_text,
            "result": result,
        }
    )

    if st.session_state.chat_order[0] != st.session_state.current_chat_id:
        st.session_state.chat_order = [st.session_state.current_chat_id] + [cid for cid in st.session_state.chat_order if cid != st.session_state.current_chat_id]

    st.rerun()
