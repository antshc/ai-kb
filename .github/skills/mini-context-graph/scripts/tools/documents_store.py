from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

_DOCUMENTS_FILE = config.DATA_DIR / "documents.json"
_CHUNK_SIZE = 500
_CHUNK_OVERLAP = 100
_STOPWORDS = {"a", "an", "the", "is", "are", "to", "of", "in", "on", "for", "with", "and", "or", "what", "why", "how"}


def _load() -> dict:
    if _DOCUMENTS_FILE.exists():
        return json.loads(_DOCUMENTS_FILE.read_text())
    return {"documents": {}}


def _save(store: dict) -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _DOCUMENTS_FILE.write_text(json.dumps(store, indent=2))


def _chunk(content: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(content):
        end = start + _CHUNK_SIZE
        text = content[start:end].strip()
        if text:
            chunks.append(text)
        if end >= len(content):
            break
        start += _CHUNK_SIZE - _CHUNK_OVERLAP
    return chunks


def add_document(doc_id: str, title: str, source: str, content: str) -> dict:
    store = _load()
    if doc_id in store["documents"]:
        return store["documents"][doc_id]
    chunks = [
        {"chunk_id": f"{doc_id}_chunk_{index:03d}", "index": index, "text": text}
        for index, text in enumerate(_chunk(content))
    ]
    document = {
        "id": doc_id,
        "title": title,
        "source": source,
        "content": content,
        "chunks": chunks,
        "ingestion_date": datetime.now(timezone.utc).isoformat(),
    }
    store["documents"][doc_id] = document
    _save(store)
    return document


def get_document(doc_id: str) -> dict | None:
    return _load()["documents"].get(doc_id)


def get_chunk(chunk_id: str) -> dict | None:
    for document in _load()["documents"].values():
        for chunk in document["chunks"]:
            if chunk["chunk_id"] == chunk_id:
                return chunk
    return None


def list_documents() -> list[dict]:
    return [
        {
            "id": document["id"],
            "title": document["title"],
            "source": document["source"],
            "chunk_count": len(document["chunks"]),
            "ingestion_date": document["ingestion_date"],
        }
        for document in _load()["documents"].values()
    ]


def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_tokens = set(re.findall(r"[a-z0-9]+", query.lower())) - _STOPWORDS
    results = []
    for document in _load()["documents"].values():
        for chunk in document["chunks"]:
            tokens = set(re.findall(r"[a-z0-9]+", chunk["text"].lower()))
            overlap = len(query_tokens & tokens)
            if overlap:
                results.append({
                    "chunk_id": chunk["chunk_id"],
                    "doc_id": document["id"],
                    "doc_title": document["title"],
                    "score": overlap / max(len(query_tokens), 1),
                    "text": chunk["text"],
                })
    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]
