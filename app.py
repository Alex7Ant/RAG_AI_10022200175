# Student Name: Alexandre Anthony
# Student Index: 10022200175

import streamlit as st

from src.pipeline import answer_query


st.set_page_config(page_title="Academic City Manual RAG", layout="wide")
st.title("Academic City Manual RAG Assistant")
st.caption("Manual implementation: chunking, retrieval, and prompt construction without LangChain/LlamaIndex.")


query = st.text_input("Ask a question", placeholder="Example: What are the key budget priorities for 2025?")
run = st.button("Submit")

if run and query.strip():
    with st.spinner("Running retrieval and generation..."):
        result = answer_query(query.strip())

    st.subheader("Final Response")
    st.write(result["answer"])

    st.subheader("Retrieved Chunks")
    for i, r in enumerate(result["retrieved"], start=1):
        st.markdown(
            f"**{i}. {r['chunk_id']}** | score={r['final_score']:.4f} "
            f"(vector={r['vector_score']:.4f}, keyword={r['keyword_score']:.4f})"
        )
        st.caption(f"Source: {r['source']}")
        st.write(r["text"])

    with st.expander("Prompt Sent to LLM"):
        st.code(result["prompt"])

    with st.expander("Selected Context Chunks"):
        for c in result["selected_context"]:
            st.write(f"- {c['chunk_id']}")
