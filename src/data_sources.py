# Student Name: Alexandre Anthony
# Student Index: 10022200175

from pathlib import Path
from typing import Dict, List

import csv
from pypdf import PdfReader


def _clean_text(text: str) -> str:
    compact = " ".join((text or "").split())
    return compact.strip()


def load_csv_rows(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV dataset not found: {csv_path}")

    seen = set()
    records: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row_idx, row in enumerate(reader):
            normalized_row = {k: ("" if row.get(k) is None else str(row.get(k))) for k in fieldnames}
            sig = tuple((k, normalized_row[k]) for k in fieldnames)
            if sig in seen:
                continue
            seen.add(sig)

            parts = [f"{col}: {normalized_row[col]}" for col in fieldnames]
            text = _clean_text(" | ".join(parts))
            records.append(
                {
                    "doc_id": f"csv_row_{row_idx}",
                    "source": str(csv_path),
                    "text": text,
                    "meta": {
                        "type": "csv",
                        "row_index": int(row_idx),
                        "columns": list(fieldnames),
                    },
                }
            )
    return records


def load_pdf_pages(pdf_path: Path, max_pages: int | None = None) -> List[Dict[str, str]]:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF dataset not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: List[Dict[str, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        if max_pages is not None and i > max_pages:
            break
        raw = page.extract_text() or ""
        text = _clean_text(raw)
        if not text:
            continue
        pages.append(
            {
                "doc_id": f"pdf_page_{i}",
                "source": str(pdf_path),
                "text": text,
                "meta": {"type": "pdf", "page": i},
            }
        )
    return pages