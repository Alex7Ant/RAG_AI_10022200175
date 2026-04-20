# Student Name: Alexandre Anthony
# Student Index: 10022200175

from dataclasses import dataclass
from pathlib import Path
import os

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv() -> None:
        return None


load_dotenv()


@dataclass
class AppConfig:
    student_name: str
    student_index: str
    llm_provider: str
    openai_api_key: str
    openai_model: str
    ollama_base_url: str
    ollama_model: str
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    hybrid_alpha: float
    data_csv_path: Path
    data_pdf_path: Path
    artifacts_dir: Path
    index_path: Path
    chunks_path: Path
    logs_path: Path
    experiments_path: Path


def load_config() -> AppConfig:
    artifacts_dir = Path("artifacts")
    return AppConfig(
        student_name=os.getenv("STUDENT_NAME", "Alexandre Anthony"),
        student_index=os.getenv("STUDENT_INDEX", "10022200175"),
        llm_provider=os.getenv("LLM_PROVIDER", "ollama").strip().lower(),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "900")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "120")),
        top_k=int(os.getenv("TOP_K", "5")),
        hybrid_alpha=float(os.getenv("HYBRID_ALPHA", "0.75")),
        data_csv_path=Path(os.getenv("DATA_CSV_PATH", "./data/raw/Ghana_Election_Result.csv")),
        data_pdf_path=Path(
            os.getenv(
                "DATA_PDF_PATH",
                "./data/raw/2025-Budget-Statement-and-Economic-Policy_v4.pdf",
            )
        ),
        artifacts_dir=artifacts_dir,
        index_path=artifacts_dir / "index.faiss",
        chunks_path=artifacts_dir / "chunks.jsonl",
        logs_path=artifacts_dir / "logs" / "pipeline_events.jsonl",
        experiments_path=artifacts_dir / "experiments",
    )