# Part F Architecture and System Design

## Data Flow
User Query -> Query Expansion -> Embedding -> Vector Retrieval -> Hybrid Scoring -> Context Selection -> Prompt Builder -> LLM -> UI Response

## Components
1. Data loaders for CSV/PDF
2. Chunking strategies (fixed, sentence)
3. Embedding engine
4. Vector index and similarity search
5. Retrieval re-scoring and query expansion
6. Prompt manager with hallucination control
7. LLM client
8. Logging layer
9. Streamlit presentation layer

## Suitability Justification
- Mixed data sources (tabular election + long policy PDF) require robust chunking and retrieval.
- Hybrid retrieval improves precision when semantic similarity alone is weak.
- Logging supports transparent analysis and manual experiment documentation.
