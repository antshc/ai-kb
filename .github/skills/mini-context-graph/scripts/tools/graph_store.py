from __future__ import annotations

import json
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

_GRAPH_FILE = config.DATA_DIR / "graph.json"


def _load() -> dict:
    if _GRAPH_FILE.exists():
        return json.loads(_GRAPH_FILE.read_text())
    return {"nodes": {}, "edges": []}


def _save(graph: dict) -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _GRAPH_FILE.write_text(json.dumps(graph, indent=2))


def add_node(name: str, node_type: str, source_document: str | None = None, source_chunks: list[str] | None = None) -> str:
    graph = _load()
    normalized = name.strip().lower()
    for node_id, node in graph["nodes"].items():
        if node["name"] == normalized:
            if source_document and not node.get("source_document"):
                node["source_document"] = source_document
            node["source_chunks"] = sorted(set(node.get("source_chunks", [])) | set(source_chunks or []))
            _save(graph)
            return node_id
    node_id = str(uuid.uuid4())[:8]
    graph["nodes"][node_id] = {
        "name": normalized,
        "type": node_type.strip().lower(),
        "source_document": source_document,
        "source_chunks": source_chunks or [],
    }
    _save(graph)
    return node_id


def add_edge(source_id: str, target_id: str, relation: str, confidence: float, source_document: str | None = None, supporting_text: str | None = None, chunk_id: str | None = None) -> None:
    graph = _load()
    relation = relation.strip().lower()
    for edge in graph["edges"]:
        if edge["source"] == source_id and edge["target"] == target_id and edge["type"] == relation:
            edge["confidence"] = max(edge["confidence"], confidence)
            edge["source_document"] = edge.get("source_document") or source_document
            edge["supporting_text"] = edge.get("supporting_text") or supporting_text
            edge["chunk_id"] = edge.get("chunk_id") or chunk_id
            _save(graph)
            return
    graph["edges"].append({
        "source": source_id,
        "target": target_id,
        "type": relation,
        "confidence": confidence,
        "source_document": source_document,
        "supporting_text": supporting_text,
        "chunk_id": chunk_id,
    })
    _save(graph)


def find_node_by_name(name: str) -> str | None:
    normalized = name.strip().lower()
    for node_id, node in _load()["nodes"].items():
        if node["name"] == normalized:
            return node_id
    return None


def get_neighbors(node_id: str, min_confidence: float = 0.0) -> list[str]:
    neighbors = set()
    for edge in _load()["edges"]:
        if edge["confidence"] < min_confidence:
            continue
        if edge["source"] == node_id:
            neighbors.add(edge["target"])
        elif edge["target"] == node_id:
            neighbors.add(edge["source"])
    return list(neighbors)


def get_subgraph(node_ids: list[str]) -> dict:
    graph = _load()
    selected = set(node_ids)
    return {
        "nodes": {node_id: graph["nodes"][node_id] for node_id in selected if node_id in graph["nodes"]},
        "edges": [edge for edge in graph["edges"] if edge["source"] in selected and edge["target"] in selected],
    }
