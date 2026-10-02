from __future__ import annotations

import os
from typing import Any, Dict, List

import chromadb

from app.config import get_settings

settings = get_settings()


class ChromaKnowledgeStore:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
        self.collection = self.client.get_or_create_collection(name=settings.vector_collection)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas)

    def search_documents(self, query: str, limit: int = 5, metadata_filter: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
        kwargs: Dict[str, Any] = {"query_texts": [query], "n_results": limit}
        if metadata_filter:
            kwargs["where"] = metadata_filter
        results = self.collection.query(**kwargs)
        output: List[Dict[str, Any]] = []
        for idx, document in enumerate(results.get("documents", [[]])[0]):
            metadata = results.get("metadatas", [[{}]])[0][idx]
            output.append({
                "document": document,
                "metadata": metadata,
                "distance": results.get("distances", [[0.0]])[0][idx],
            })
        return output

    def delete_document(self, document_id: str) -> None:
        self.collection.delete(ids=[document_id])
