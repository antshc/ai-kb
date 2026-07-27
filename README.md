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

Install Graphify with the package manager of your choice if `graphify` is not
already available, then build the corpus from the repository root:

```powershell
$env:GRAPHIFY_OUT = "graphify-out"
graphify extract raw --out . --wiki
```

Update the graph after raw documents change:

```powershell
$env:GRAPHIFY_OUT = "graphify-out"
graphify extract raw --out . --update --wiki
```

Query the generated graph:

```powershell
graphify query "<question>"
graphify path "<concept-a>" "<concept-b>"
graphify explain "<concept>"
```

Graphify output is generated and reviewable. Do not edit `raw/` during graph
generation, and do not commit `graphify-out/cache/` or `graphify-out/cost.json`.
