---
name: mini-context-graph
description: |
  A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern
  with a structured knowledge graph. Ingest documents once — the LLM writes wiki
  pages, extracts entities/relations into the graph, and stores raw content for
  evidence retrieval. Knowledge accumulates and cross-references; it is never
  re-derived from scratch.
---

# Mini Context Graph Skill

## The Core Idea

Standard RAG re-discovers knowledge from scratch on every query. This skill is different:

1. **Wiki layer** — The LLM writes and maintains persistent markdown pages (summaries, entity pages, topic syntheses). Cross-references are already there. The wiki gets richer with every ingest.
2. **Graph layer** — Entities and relations are extracted once and stored as a navigable knowledge graph. BFS traversal answers structural queries without re-reading sources.
3. **Raw source layer** — Original documents are stored immutably with chunks. Provenance links tie every graph node and edge back to the exact text that supports it.

> The LLM writes; the Python tools handle all bookkeeping.

## Three Layers

| Layer | Where | What the LLM does | What Python does |
|-------|-------|-------------------|-----------------|
| **Raw Sources** | `data/documents.json` | Reads (never modifies) | Stores chunks + metadata |
| **Wiki** | `wiki/` (markdown) | Writes/updates pages | Manages index.md + log.md |
| **Graph** | `data/graph.json` | Extracts entities + relations | Persists, deduplicates, traverses |

## Quick Start for Agents

```python
from scripts.contextgraph import ContextGraphSkill
from scripts.tools import wiki_store

skill = ContextGraphSkill()

entities = [
    {"name": "memory leak", "type": "issue", "supporting_text": "memory leaks cause crashes"},
    {"name": "system crash", "type": "issue", "supporting_text": "system crashes due to memory leaks"},
]
relations = [
    {"source": "memory leak", "target": "system crash", "type": "causes",
     "confidence": 1.0, "supporting_text": "System crashes due to memory leaks."},
]

result = skill.ingest_with_content(
    doc_id="doc_001",
    title="System Crash Analysis",
    source="/docs/incident_report.pdf",
    raw_content="System crashes due to memory leaks. Memory leaks occur when objects are not released.",
    entities=entities,
    relations=relations,
)

pages = wiki_store.search_wiki("memory leak")
result = skill.query_with_evidence("Why does the system crash?")
```

## Operations

### Ingest

When a user provides a new document:

1. Read `references/ingestion.md`.
2. Read `references/ontology.md`.
3. Extract entities and relations using LLM reasoning.
4. Call `skill.ingest_with_content(...)`.
5. Write a wiki summary page using `wiki_store.write_page(category="summary", ...)`.
6. Write or update entity pages.
7. Update topic pages when applicable.

### Query

1. Check the wiki first with `wiki_store.search_wiki(query)`.
2. Synthesize from wiki pages when sufficient.
3. Otherwise call `skill.query_with_evidence(query)`.
4. Return evidence from supporting documents.
5. File valuable answers back into a topic page.

### Lint

```python
from scripts.tools import wiki_store
issues = wiki_store.lint_wiki()
```

Review broken links, orphan pages, stale claims, contradictions, and missing cross-references. See `references/lint.md`.

## Ingestion Constraints

- Do not hallucinate entities not present in the text.
- Do not add relations without explicit textual evidence.
- Do not add edges with confidence below `0.6`.
- Provide `supporting_text` for every entity and relation.
- Write a wiki summary page for every ingested document.
- Update existing entity pages when new information arrives.
- Flag contradictions when sources conflict.

## Retrieval Constraints

- Traversal depth must not exceed `2`.
- Traverse only edges with confidence at least `0.6`.
- Return at most `50` nodes.
- Do not fabricate nodes or edges.

## Python API

| Method | Purpose |
|--------|---------|
| `ingest_with_content(...)` | Store raw content, graph entities, relations, and provenance |
| `add_node(...)` | Add a graph entity |
| `add_edge(...)` | Add a graph relation |
| `query(...)` | Retrieve a graph subgraph |
| `query_with_evidence(...)` | Retrieve graph context with source chunks |
| `wiki_store.write_page(...)` | Write or update a wiki page |
| `wiki_store.search_wiki(...)` | Search the wiki first |
| `wiki_store.lint_wiki()` | Check wiki health |
| `documents_store.search_chunks(...)` | Search raw evidence chunks |

## Design Philosophy

| Layer | Owner |
|-------|-------|
| Extraction, synthesis, and wiki writing | Agent guidance |
| Wiki index, log, and file I/O | `wiki_store.py` |
| Graph persistence and BFS traversal | Graph tools |
| Raw documents, chunks, and provenance | `documents_store.py` |

The human curates sources and asks questions. The agent writes the wiki, extracts the graph, and answers with citations. Python handles deterministic bookkeeping.
