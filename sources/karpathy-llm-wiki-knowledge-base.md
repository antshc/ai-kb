# Karpathy LLM Wiki: Knowledge-Base Skill Comparison

> Research snapshot: 2026-07-27

## Summary

For a GitHub Copilot-based knowledge repository, **`mini-context-graph` is the best-fit Karpathy LLM Wiki skill**.

It directly implements the core pattern as an installable Agent Skill:

- persistent, LLM-maintained Markdown wiki;
- structured knowledge graph;
- immutable raw sources;
- provenance and source evidence;
- incremental ingestion;
- wiki search, graph queries, linting, and contradiction handling.

The strongest alternatives serve different use cases:

| Project | Best for | Assessment |
|---|---|---|
| [`mini-context-graph`](https://awesome-copilot.github.com/skill/mini-context-graph/) | GitHub Copilot Agent Skills | Best fit for this repository |
| [`atomicstrata/llm-wiki-compiler`](https://github.com/atomicstrata/llm-wiki-compiler) | Full standalone knowledge compiler | Most complete implementation reviewed |
| [`ussumant/llm-wiki-compiler`](https://github.com/ussumant/llm-wiki-compiler) | Claude Code and Codex workflows | Strong plugin-first compilation workflow |
| [`Graphify`](https://github.com/Graphify-Labs/graphify) | Codebase understanding | Best code-first graph tool; not primarily an LLM Wiki |

## Karpathy's LLM Wiki Pattern

Andrej Karpathy describes an LLM Wiki as a persistent, interlinked Markdown knowledge base maintained by an LLM agent.

Unlike conventional retrieval-augmented generation, which retrieves raw chunks and reconstructs an answer for each query, the LLM Wiki compiles knowledge during ingestion. The resulting synthesis is retained, updated, cross-linked, and reused.

### Core layers

```text
Raw sources
    ↓
Persistent wiki
    ↓
Agents and users
```

Karpathy's original architecture includes three conceptual layers:

1. **Raw sources** — immutable, human-curated source material.
2. **Wiki** — LLM-generated summaries, entity pages, concept pages, comparisons, and syntheses.
3. **Schema** — instructions defining structure, conventions, ingestion, querying, and maintenance.

Implementations may add a knowledge graph and search index:

```text
Immutable sources
    ↓
Persistent wiki
    ↓
Knowledge graph and search index
    ↓
Evidence-backed agent queries
```

### Main operations

- **Ingest:** read a source, create its summary, update related pages, add cross-references, and record provenance.
- **Query:** search existing synthesis first, inspect supporting evidence as needed, and optionally preserve valuable answers as new wiki content.
- **Lint:** detect contradictions, stale claims, orphan pages, missing links, weak coverage, and unresolved research gaps.

Source: [Andrej Karpathy — LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Why `mini-context-graph` Is the Best Copilot Skill

`mini-context-graph` closely matches the LLM Wiki pattern while adding structured retrieval and provenance.

### Architecture

1. **Wiki layer** — persistent summaries, entity pages, and topic syntheses.
2. **Graph layer** — entities and relations extracted once for structural traversal.
3. **Raw-source layer** — immutable source documents and chunks retained for evidence retrieval.

### Strengths

- Distributed as a native Agent Skill in `github/awesome-copilot`.
- Works naturally with repository-local `SKILL.md` workflows.
- Keeps the human-readable wiki as the primary synthesis artifact.
- Adds graph traversal without replacing Markdown with an opaque database.
- Preserves exact source evidence for claims and relations.
- Supports search, evidence retrieval, graph queries, document listing, and linting.
- Fits Git-based review, history, branching, and collaboration.

### Trade-offs

- Ingestion remains agent-guided rather than a fully autonomous compiler pipeline.
- Graph quality depends on disciplined ontology and extraction rules.
- Larger corpora may eventually require stronger semantic retrieval and reranking.

References:

- [Mini Context Graph skill](https://awesome-copilot.github.com/skill/mini-context-graph/)
- [Awesome GitHub Copilot repository](https://github.com/github/awesome-copilot)

## Alternative Implementations

### `atomicstrata/llm-wiki-compiler`

The most complete standalone implementation reviewed.

Notable capabilities:

- typed wiki pages such as concepts, entities, comparisons, and overviews;
- paragraph- and claim-level citations;
- semantic embeddings and incremental content hashing;
- BM25 reranking;
- wiki-link graph expansion;
- multiple model providers, including GitHub Copilot;
- CLI and agent-oriented workflows.

Choose it when retrieval quality, compilation automation, provider portability, and a complete standalone runtime matter more than keeping the implementation as a lightweight repository skill.

Reference: [`atomicstrata/llm-wiki-compiler`](https://github.com/atomicstrata/llm-wiki-compiler)

### `ussumant/llm-wiki-compiler`

A plugin-first implementation for Claude Code and Codex.

Notable capabilities:

- topic-based knowledge compilation;
- knowledge-project and codebase modes;
- concept discovery and schema generation;
- coverage and staleness workflows;
- knowledge-graph visualization;
- Claude Code and Codex-compatible packaging.

Choose it when the primary environment is Claude Code or Codex and the desired interaction model is a guided compiler workflow.

Reference: [`ussumant/llm-wiki-compiler`](https://github.com/ussumant/llm-wiki-compiler)

### Graphify

Graphify is a strong codebase-understanding tool rather than a direct LLM Wiki implementation.

Notable capabilities:

- deterministic AST parsing with Tree-sitter;
- queryable code and document knowledge graph;
- explicit distinction between extracted and inferred edges;
- no required vector database for code structure;
- optional Markdown wiki generation;
- integrations with Copilot, Claude Code, Codex, Cursor, and other agents.

Choose it when the primary problem is understanding code structure, dependencies, schemas, and architecture. Combine it with an LLM Wiki when both code intelligence and durable research synthesis are required.

Reference: [`Graphify-Labs/graphify`](https://github.com/Graphify-Labs/graphify)

## Decision

Use **`mini-context-graph`** for this repository because it provides the best balance of:

- direct alignment with Karpathy's pattern;
- native GitHub Copilot skill integration;
- persistent Markdown synthesis;
- graph-based structural queries;
- immutable evidence and provenance;
- lightweight, repository-local operation.

Consider `atomicstrata/llm-wiki-compiler` if the repository outgrows the current retrieval model and requires semantic top-K retrieval, reranking, automated compilation, or broader provider support.

## Skill-Design Notes

Effective Agent Skills should remain concise, use progressive disclosure, provide specific discovery metadata, separate detailed references from the main `SKILL.md`, and include validation loops for fragile workflows.

The current `mini-context-graph` structure follows this model by keeping the skill entry point focused and moving ingestion, ontology, retrieval, and linting details into reference files and scripts.

Reference: [Anthropic — Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
