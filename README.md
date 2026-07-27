# Knowledge Base

This repository stores an immutable raw document corpus and a generated
[Graphify](https://github.com/Graphify-Labs/graphify) knowledge graph.

## Layout

```text
raw/                         Immutable source documents
graphify-out/                Generated graph, report, visualization, and wiki
.codex/skills/graphify/      Codex project integration
.copilot/skills/graphify/    GitHub Copilot project integration
```

## Usage

Ask Codex or Copilot explicitly:

- “Ingest `raw/` and update the Graphify knowledge base.”
- “Refresh Graphify lessons if stale.”
- “Search the knowledge base for `<question>`.”

No local auto-ingestion. GitHub Actions ingests after pushes to `main` changing
`raw/**`.

Graphify output is generated and reviewable. Do not edit `raw/` during graph
generation, and do not commit `graphify-out/cache/` or `graphify-out/cost.json`.
