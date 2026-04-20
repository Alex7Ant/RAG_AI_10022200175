# Student Name: Alexandre Anthony
# Student Index: 10022200175

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def log_event(log_path: Path, stage: str, payload: Dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "stage": stage,
        "payload": payload,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")