# Manual RAG Chatbot for Academic City (CS4241)

Student Name: Alexandre Anthony  
Student Index: 10022200175

This project is a manual RAG implementation that avoids end-to-end frameworks such as LangChain and LlamaIndex.

## 1. What This Implements

- Data loading and cleaning for CSV and PDF sources.
- Two chunking strategies for comparison.
- Embedding pipeline using sentence-transformers.
- Vector store and similarity retrieval using FAISS.
- Query expansion extension to improve retrieval.
- Prompt construction with hallucination control instructions.
- Full pipeline logging: query, retrieval, context selection, prompt, and final response.
- Streamlit app showing retrieved chunks, similarity scores, prompt, and answer.
- Evaluation script for adversarial tests and RAG vs non-retrieval baseline.

## 2. Quick Start (Finish Fast)

1. Create and activate a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` and fill values.
4. Put dataset files into `data/raw/`:
   - `Ghana_Election_Result.csv`
   - `2025-Budget-Statement-and-Economic-Policy_v4.pdf`
5. Build chunks and vector index.
6. Run Streamlit app.

## 3. Commands

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

python scripts/ingest.py --strategy fixed
streamlit run app.py
```

To compare chunking strategies:

```bash
python scripts/ingest.py --strategy fixed
python scripts/ingest.py --strategy sentence
```

To run adversarial evaluation:

```bash
python scripts/evaluate.py
```

## 4. Suggested 2-Day Execution Plan

### Day 1

1. Set up environment and ingest both files.
2. Run retrieval tests and collect failure cases.
3. Tune chunk size and overlap with evidence.
4. Tune query expansion and top-k.

### Day 2

1. Finalize prompt variants and compare outputs.
2. Capture screenshots and manual logs.
3. Record short walkthrough video (<= 2 minutes).
4. Deploy app and push final repository.

## 5. Mapping to Marking Rubric

- Part A: `scripts/ingest.py`, `src/chunking.py`, logs in `artifacts/experiments/`.
- Part B: `src/embeddings.py`, `src/vector_index.py`, `src/retrieval.py`.
- Part C: `src/prompting.py` and prompt experiment notes.
- Part D: `src/pipeline.py`, `artifacts/logs/pipeline_events.jsonl`.
- Part E: `scripts/evaluate.py`, `docs/experiment_log_template.md`.
- Part F: `docs/architecture.md` and architecture diagram.
- Part G: Query expansion in `src/retrieval.py` (can extend to feedback loop).

## 6. Submission Checklist

- Include your name and index in all files before final submission.
- Add collaborator: `godwin.danso@acity.edu.gh` or `GodwinDansoAcity`.
- Share repository link, deployed URL, and documentation by email.
