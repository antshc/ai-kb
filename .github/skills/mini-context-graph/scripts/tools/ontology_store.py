from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

_ONTOLOGY_FILE = config.DATA_DIR / "ontology.json"

_ENTITY_TYPES = {
    "module": "component", "class": "component", "function": "component", "method": "component",
    "bug": "issue", "defect": "issue", "error": "issue", "failure": "issue", "problem": "issue",
    "server": "infrastructure", "host": "infrastructure", "machine": "infrastructure", "node": "infrastructure",
    "user": "actor", "person": "actor", "operator": "actor", "admin": "actor",
    "app": "software", "application": "software", "service": "software", "program": "software", "library": "software", "package": "software",
    "database": "storage", "datastore": "storage", "db": "storage",
    "api": "interface", "endpoint": "interface", "connection": "interface",
    "incident": "event", "occurrence": "event", "trigger": "event",
    "idea": "concept", "principle": "concept", "theory": "concept",
    "thread": "process", "task": "process", "job": "process", "workflow": "process",
}

_RELATIONS = {
    "triggers": "causes", "leads to": "causes", "results in": "causes", "produces": "causes",
    "is part of": "contains", "belongs to": "contains", "lives in": "contains",
    "requires": "depends on", "needs": "depends on",
    "calls": "uses", "invokes": "uses", "consumes": "uses",
    "impacts": "affects", "influences": "affects",
    "instantiates": "creates", "spawns": "creates",
    "links to": "connects to", "references": "connects to",
    "inherits from": "extends", "subclasses": "extends",
    "queries": "reads from", "fetches": "reads from",
    "stores in": "writes to", "persists to": "writes to",
}


def _load() -> dict:
    if _ONTOLOGY_FILE.exists():
        return json.loads(_ONTOLOGY_FILE.read_text())
    return {"entity_types": {}, "relation_types": {}}


def _save(ontology: dict) -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _ONTOLOGY_FILE.write_text(json.dumps(ontology, indent=2))


def _normalize(value: str) -> str:
    return value.strip().lower().replace("-", " ").replace("_", " ")


def normalize_type(type_name: str) -> str:
    value = _normalize(type_name)
    return _ENTITY_TYPES.get(value, value)


def normalize_relation(relation_name: str) -> str:
    value = _normalize(relation_name)
    return _RELATIONS.get(value, value)


def add_type(type_name: str) -> None:
    ontology = _load()
    value = normalize_type(type_name)
    ontology["entity_types"][value] = ontology["entity_types"].get(value, 0) + 1
    _save(ontology)


def add_relation(relation_name: str) -> None:
    ontology = _load()
    value = normalize_relation(relation_name)
    ontology["relation_types"][value] = ontology["relation_types"].get(value, 0) + 1
    _save(ontology)


def get_all_types() -> dict[str, int]:
    return _load()["entity_types"]


def get_all_relations() -> dict[str, int]:
    return _load()["relation_types"]
