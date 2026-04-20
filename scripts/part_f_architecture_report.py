# Student Name: Alexandre Anthony
# Student Index: 10022200175

from pathlib import Path


def main() -> None:
    out_dir = Path("artifacts/experiments")
    out_dir.mkdir(parents=True, exist_ok=True)

    report = (
        "# Part F Architecture and System Design\n\n"
        "## Data Flow\n"
        "User Query -> Query Expansion -> Embedding -> Vector Retrieval -> "
        "Hybrid Scoring -> Context Selection -> Prompt Builder -> LLM -> UI Response\n\n"
        "## Components\n"
        "1. Data loaders for CSV/PDF\n"
        "2. Chunking strategies (fixed, sentence)\n"
        "3. Embedding engine\n"
        "4. Vector index and similarity search\n"
        "5. Retrieval re-scoring and query expansion\n"
        "6. Prompt manager with hallucination control\n"
        "7. LLM client\n"
        "8. Logging layer\n"
        "9. Streamlit presentation layer\n\n"
        "## Suitability Justification\n"
        "- Mixed data sources (tabular election + long policy PDF) require robust chunking and retrieval.\n"
        "- Hybrid retrieval improves precision when semantic similarity alone is weak.\n"
        "- Logging supports transparent analysis and manual experiment documentation.\n"
    )

    out_md = out_dir / "part_f_architecture_report.md"
    out_md.write_text(report, encoding="utf-8")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()