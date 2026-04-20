# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.config import load_config
from src.pipeline import answer_query


def main() -> None:
    cfg = load_config()
    query = "Compare election and fiscal policy themes from the provided sources."
    result = answer_query(query)

    report = {
        "part": "D",
        "query": query,
        "retrieved_count": len(result["retrieved"]),
        "selected_context_count": len(result["selected_context"]),
        "prompt_preview": result["prompt"][:1200],
        "answer_preview": result["answer"][:1200],
        "log_file": str(cfg.logs_path),
    }

    cfg.experiments_path.mkdir(parents=True, exist_ok=True)
    out_json = cfg.experiments_path / "part_d_pipeline_report.json"
    out_md = cfg.experiments_path / "part_d_pipeline_report.md"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(
        "# Part D Full RAG Pipeline Report\n\n"
        "- Pipeline executed end-to-end: query -> retrieval -> context -> prompt -> response.\n"
        f"- Retrieved chunks: {len(result['retrieved'])}\n"
        f"- Selected context chunks: {len(result['selected_context'])}\n"
        f"- Logs written to: {cfg.logs_path}\n",
        encoding="utf-8",
    )

    print(f"Saved: {out_json}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()