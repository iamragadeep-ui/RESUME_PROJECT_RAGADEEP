from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from app.rag.vector_store import ChromaKnowledgeStore


class KnowledgeAgent:
    def __init__(self, persist_dir: str | None = None) -> None:
        self.store = ChromaKnowledgeStore()

    def ingest_file(self, file_path: str) -> None:
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        chunks = [
            {
                "id": f"{path.stem}-{i}",
                "text": chunk,
                "metadata": {"source": str(path), "title": path.stem, "category": "policy"},
            }
            for i, chunk in enumerate([content])
        ]
        self.store.add_documents(chunks)

    def search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        results = self.store.search_documents(query, limit=limit)
        return results
