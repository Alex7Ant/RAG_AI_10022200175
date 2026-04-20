# Parts A-F Execution Guide

Student Name: Alexandre Anthony  
Student Index: 10022200175

## Part A: Data Engineering and Preparation

1. Download datasets:
   - `python scripts/download_datasets.py`
2. Run ingestion with two chunk strategies:
   - `python scripts/ingest.py --strategy fixed`
   - `python scripts/ingest.py --strategy sentence`
3. Generate comparative analysis:
   - `python scripts/part_a_compare_chunking.py`
4. Collect outputs:
   - `artifacts/experiments/part_a_chunking_comparison.json`
   - `artifacts/experiments/part_a_chunking_comparison.md`

## Part B: Custom Retrieval System

Implemented in:
- `src/embeddings.py`
- `src/vector_index.py`
- `src/retrieval.py`

What to demonstrate:
1. Top-k retrieval with similarity scores.
2. Query expansion extension.
3. Failure case and fix:
   - Capture one irrelevant retrieval example.
   - Tune `HYBRID_ALPHA` or expand query terms in `src/retrieval.py`.
   - Show before/after evidence in manual logs.

## Part C: Prompt Engineering and Generation

Implemented in:
- `src/prompting.py`

What to demonstrate:
1. Context injection.
2. Hallucination control instruction.
3. Prompt iteration evidence:
   - Modify answer format and grounding rules.
   - Run same query and compare output quality.

## Part D: Full RAG Pipeline

Implemented in:
- `src/pipeline.py`
- `src/logging_utils.py`

What to show:
1. Full flow: query -> retrieval -> context -> prompt -> response.
2. Logs in `artifacts/logs/pipeline_events.jsonl`.
3. Retrieved docs, scores, and final prompt in the UI.

## Part E: Critical Evaluation and Adversarial Testing

Run:
- `python scripts/evaluate.py`

What to show:
1. Two adversarial queries.
2. RAG vs baseline (no retrieval).
3. Evidence-based analysis using generated report and manual judgments.

## Part F: Architecture and System Design

Use:
- `docs/architecture.md`

What to submit:
1. Component diagram and data flow.
2. Design justifications tied to dataset characteristics.
3. Why your architecture fits this domain.
