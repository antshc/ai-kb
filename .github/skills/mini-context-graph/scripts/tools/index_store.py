from __future__ import annotations

import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

_INDEX_FILE = config.DATA_DIR / "index.json"
_STOPWORDS = {"a", "an", "the", "is", "are", "to", "of", "in", "on", "for", "with", "and", "or", "what", "why", "how"}


def _load() -> dict:
    if _INDEX_FILE.exists():
        return json.loads(_INDEX_FILE.read_text())
    return {"entity_index": {}, "keyword_index": {}}


def _save(index: dict) -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _INDEX_FILE.write_text(json.dumps(index, indent=2))


def _tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in _STOPWORDS and len(token) > 1]


def add_entity(name: str, node_id: str) -> None:
    index = _load()
    normalized = name.strip().lower()
    index["entity_index"].setdefault(normalized, [])
    if node_id not in index["entity_index"][normalized]:
        index["entity_index"][normalized].append(node_id)
    for token in _tokens(normalized):
        index["keyword_index"].setdefault(token, [])
        if node_id not in index["keyword_index"][token]:
            index["keyword_index"][token].append(node_id)
    _save(index)


def search(query: str) -> list[str]:
    index = _load()
    normalized = query.strip().lower()
    matches = set(index["entity_index"].get(normalized, []))
    for token in _tokens(normalized):
        matches.update(index["keyword_index"].get(token, []))
    return list(matches)
