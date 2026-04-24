# Manual RAG Chatbot for Academic City (CS4241)

**Student Name:** Alexandre Anthony  
**Student Index:** 10022200175

## Abstract

This project implements a manual Retrieval-Augmented Generation (RAG) system for answering questions over two source types: a Ghana election results dataset and the 2025 State of the Nation / budget document. The system is built without end-to-end RAG frameworks such as LangChain or LlamaIndex. Instead, it uses custom data loading, preprocessing, chunking, embedding, retrieval, prompt construction, logging, evaluation, and a Streamlit user interface. The final system supports transparent evidence-based answering, showing retrieved chunks, similarity scores, and prompt content for each response.

The work demonstrates the complete RAG lifecycle: data preparation, comparison of chunking strategies, hybrid retrieval with query expansion, prompt engineering, adversarial testing, and system design justification. The final application is designed to be inspectable and suitable for manual evaluation in an academic setting.

## 1. Introduction

The goal of this project is to build a transparent and manually controlled RAG pipeline that can answer questions using local documents while exposing the intermediate steps that led to each answer. The repository is structured to support a final-year examination workflow, where each part of the system can be demonstrated independently and documented with evidence.

The project is intentionally modular. Each stage of the pipeline is implemented in a separate file, making it possible to inspect and evaluate the behavior of data ingestion, chunking, retrieval, prompting, and response generation. This is especially important for academic assessment because it allows the system to be explained, debugged, and justified in a principled way.

## 2. Datasets and Preprocessing

The repository uses two main sources:

1. `data/raw/Ghana_Election_Result.csv`
2. `data/raw/2025-Budget-Statement-and-Economic-Policy_v4.pdf`

The preprocessing pipeline performs lightweight but necessary cleaning so the documents are suitable for retrieval:

- CSV rows are normalized into clean text records.
- Duplicate CSV rows are removed by exact row signature.
- PDF pages are extracted and whitespace is compacted.
- Empty PDF pages are skipped.
- Records are converted into a common text-based representation before chunking.

This preprocessing is implemented in `src/data_sources.py`. The design is simple but appropriate for a manual RAG pipeline because the main requirement is to standardize heterogeneous sources into a retrieval-friendly format, not to perform heavy linguistic normalization.

## 3. Chunking Strategy Comparison

Part A compares two chunking strategies:

- Fixed token chunking
- Sentence-window chunking

The reported results are:

- Fixed chunk count: 664
- Fixed mean query coverage: 0.5509
- Sentence chunk count: 1631
- Sentence mean query coverage: 0.4769

These numbers show that fixed chunking produced fewer chunks but stronger average query coverage in the recorded experiment. That makes it a good default for this project because it balances retrieval granularity with better concentration of relevant terms. Sentence chunking remains useful as a comparison baseline, but the evidence in the repository favors fixed token chunking for the main pipeline.

The chunking logic is implemented in `src/chunking.py`, and the comparison output is recorded in the Part A experiment artifacts.

## 4. Embeddings and Retrieval

The embedding and retrieval layer is implemented in `src/embeddings.py`, `src/vector_index.py`, and `src/retrieval.py`.

The system uses a hybrid retrieval approach:

- Vector similarity from embeddings
- Keyword overlap scoring
- Score fusion through a configurable `HYBRID_ALPHA`
- Query expansion for selected domain terms

The retrieval configuration recorded in the repository is:

- Top-k: 5
- Default hybrid alpha: 0.75
- Extension used: query expansion + hybrid scoring

This design is suitable for the project because the corpus contains both tabular election data and long-form policy text. Pure semantic similarity is not always enough to distinguish between those source types, so hybrid scoring improves precision and gives a better chance of retrieving exact terms when needed.

A later refinement in the retrieval logic also introduced source-aware routing so that election-related questions preferentially search the CSV source and budget-related questions preferentially search the PDF source. This reduces the risk of the system repeatedly answering from the wrong document family.

## 5. Prompt Engineering and Generation

Prompt construction is implemented in `src/prompting.py`. The prompt template explicitly instructs the model to:

- Use only the provided context
- State when the answer is not found in context
- Cite supporting chunks
- Follow a structured answer format

Part C confirms that two prompt templates were tested, and the stronger version enforces grounding and citation structure. This is important because a RAG system is only useful if it stays aligned with the retrieved evidence rather than drifting into unsupported generation.

The generation layer is implemented in `src/llm_client.py`. It supports OpenAI and Ollama backends through configuration. If the configured backend is unreachable, the system falls back to an evidence-based local answer mode so the pipeline can still complete. That fallback is useful for resilience, but it also means a real API key or live LLM endpoint is required for full-quality generation.

## 6. Full Pipeline

The end-to-end pipeline is implemented in `src/pipeline.py` and logs each stage to `artifacts/logs/pipeline_events.jsonl`.

The pipeline stages are:

1. Query received
2. Retrieval
3. Context selection
4. Prompt construction
5. Response generation

Part D confirms that the pipeline executes end to end, with 5 retrieved chunks and 1 selected context chunk in the recorded run. The logging design is a strong feature of the project because it makes the pipeline auditable: each answer can be traced back to the retrieved evidence and the exact prompt sent to the model.

## 7. User Interface

The Streamlit application in `app.py` provides a user-facing interface for the RAG system. It now uses a chat-style layout with:

- A sidebar
- A new chat button
- Recent chat history
- Conversation-based message display
- Per-chat session state
- Evidence panels for retrieved chunks, prompt text, and run snapshot

This design makes the project feel much closer to a modern conversational assistant while still exposing the underlying retrieval behavior for grading and debugging. It also supports a more natural workflow for asking multiple related questions in one session.

## 8. Critical Evaluation and Adversarial Testing

Part E includes adversarial evaluation with comparison between RAG and non-retrieval baseline behavior. The evaluation process was designed to examine:

- Hallucination tendency
- Consistency
- Evidence grounding
- Sensitivity to misleading or incomplete queries

The repository records that two adversarial prompts were tested and that a RAG-versus-baseline comparison was produced. This is important because academic evaluation should not only show correct answers on easy questions; it should also show how the system behaves under difficult or ambiguous inputs.

## 9. Architecture and System Design

The architecture is intentionally modular and easy to inspect. The documented data flow is:

Query -> Query Expansion -> Embedding -> Vector Retrieval -> Hybrid Scoring -> Context Selection -> Prompt Builder -> LLM -> UI Response

The main components are:

1. Data loaders for CSV and PDF
2. Chunking strategies
3. Embedding engine
4. Vector index and similarity search
5. Retrieval re-scoring and query expansion
6. Prompt manager with hallucination control
7. LLM client
8. Logging layer
9. Streamlit presentation layer

This architecture fits the dataset because the project combines structured election data with long-form policy text. The hybrid retrieval layer helps when one document source is semantically dominant, while logging and prompt control keep the system explainable. The modular structure also makes it easier to demonstrate each part separately during a presentation or viva.

## 10. Limitations

The project is functional, but it has some limitations that should be acknowledged in a final submission:

- The election dataset is region-level, not constituency-level, so constituency questions are out of scope.
- The LLM backend depends on a reachable OpenAI or Ollama service.
- The current chat history is session-based and not permanently stored across browser restarts.
- The preprocessing is intentionally lightweight and does not include deeper linguistic normalization.

These limitations do not invalidate the project; rather, they define the boundary of what the system is meant to do in this submission.

## 11. Conclusion

This project demonstrates a complete manual RAG implementation for Academic City. It covers data preparation, chunking strategy comparison, hybrid retrieval, prompt engineering, logging, evaluation, and a chat-style user interface. The repository contains the evidence needed to explain and defend the implementation as a final-year project, and the system is structured to support transparent grading and further improvement.

## 12. Mapping to Parts A to F

- Part A: Data engineering, preprocessing, and chunking comparison
- Part B: Hybrid retrieval, query expansion, and retrieval tuning
- Part C: Prompt engineering and grounded generation
- Part D: Full pipeline execution and logging
- Part E: Adversarial evaluation and baseline comparison
- Part F: Architecture and system design justification

## 13. Key Repository References

- README summary: `README.md`
- Architecture notes: `docs/architecture.md`
- Execution guide: `docs/parts_A_to_F_execution_guide.md`
- Chunking comparison: `artifacts/experiments/part_a_chunking_comparison.md`
- Retrieval report: `artifacts/experiments/part_b_retrieval_report.md`
- Prompt experiments: `artifacts/experiments/part_c_prompt_experiments.md`
- Pipeline report: `artifacts/experiments/part_d_pipeline_report.md`
- Adversarial evaluation: `artifacts/experiments/part_e_adversarial_report.md`
- Architecture report: `artifacts/experiments/part_f_architecture_report.md`
