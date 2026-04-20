# Manual RAG Architecture

Student Name: Alexandre Anthony  
Student Index: 10022200175

## Components

1. Data Loaders (`src/data_sources.py`)
2. Chunking (`src/chunking.py`)
3. Embedding Pipeline (`src/embeddings.py`)
4. Vector Store and Similarity Search (`src/vector_index.py`)
5. Retrieval + Query Expansion (`src/retrieval.py`)
6. Prompt Construction (`src/prompting.py`)
7. LLM Interface (`src/llm_client.py`)
8. UI Layer (`app.py`)
9. Logging (`src/logging_utils.py`)

## Data Flow

User Query -> Query Expansion -> Vector Search -> Hybrid Score Fusion -> Context Selection -> Prompt Construction -> LLM Response -> UI + Logs

## Why This Design Fits This Domain

1. Dataset includes both tabular and long-form policy documents.
2. Hybrid scoring balances semantic relevance and exact keyword match.
3. Context-limited prompt reduces hallucination and token waste.
4. Stage-level logging supports auditability and error analysis.
