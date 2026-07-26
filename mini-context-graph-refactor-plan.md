# Mini Context Graph Refactor Plan

## Goal

Refactor `ai-kb` into a persistent knowledge base that uses the repository skill at `.github/skills/mini-context-graph/` for wiki-first retrieval, graph navigation, provenance, and maintenance.

## Target Structure

```text
ai-kb/
├── AGENTS.md
├── README.md
├── mini-context-graph-refactor-plan.md
│
├── .github/
│   └── skills/
│       └── mini-context-graph/
│           ├── SKILL.md
│           ├── LICENSE
│           ├── references/
│           └── scripts/
│
├── sources/
│   └── *.md
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── entities/
│   ├── summaries/
│   └── topics/
│
├── data/
│   ├── documents.json
│   ├── graph.json
│   ├── index.json
│   └── ontology.json
│
└── archive/
```

## Ownership

| Path | Owner | Purpose |
|---|---|---|
| `.github/skills/mini-context-graph/` | Maintained code | Reusable skill instructions and deterministic Python tooling |
| `sources/` | Human-maintained | Canonical source documents ingested into the graph |
| `wiki/` | Agent-maintained | Persistent summaries, entity pages, topic syntheses, and cross-references |
| `data/` | Tool-managed | Documents, chunks, graph, ontology, and search indexes |
| `archive/` | Human-maintained | Superseded or inactive source documents |

Do not create a parallel YAML graph. The installed skill owns graph persistence through `data/graph.json`, search through `data/index.json`, and ontology through `data/ontology.json`.

## Repository Rules

Add `AGENTS.md` with these rules:

- Treat `sources/` as canonical source material.
- Treat `wiki/` as maintained synthesized knowledge.
- Treat `data/` as machine-managed state.
- Search the wiki before searching raw sources.
- Use `mini-context-graph` for ingestion and graph navigation.
- Ingest every new source document.
- Create one summary page for every ingested source.
- Create or update relevant entity and topic pages.
- Do not invent entities or relations.
- Require supporting source text for every entity and relation.
- Do not manually edit `wiki/index.md` or `wiki/log.md`.
- Do not delete wiki pages or resolve contradictions without explicit human review.

## Migration Map

Create a complete migration table before moving files:

| Current file | Target source path | Stable document ID | Wiki treatment |
|---|---|---|---|
| `RAG-cheat-sheet.md` | `sources/rag-cheat-sheet.md` | `rag-cheat-sheet` | Summary, entities, RAG topic |
| `LSP Tools Reference.md` | `sources/lsp-tools-reference.md` | `lsp-tools-reference` | Summary, LSP entities, repository-search topic |
| `Improve agent robustness and resumability.md` | `sources/resumable-agent-workflows.md` | `resumable-agent-workflows` | Summary, workflow entities, reliability topic |
| `docs/agent-skill-plugin-authoring-standard.md` | `sources/agent-skill-plugin-authoring-standard.md` | `agent-skill-authoring-standard` | Summary, authoring entities, agent-skills topic |
| `docs/custom-skill-workflow-yaml.md` | `sources/custom-skill-workflow-yaml.md` | `custom-skill-workflow-yaml` | Summary, workflow entities, agent-workflows topic |

Extend the table until every active document has exactly one destination and document ID.

## Phases

### Phase 1 — Merge and Smoke-Test the Skill

1. Merge the skill PR.
2. Import `ContextGraphSkill` from the installed skill.
3. Set runtime paths to a temporary directory.
4. Ingest one synthetic document.
5. Query one entity and one relation.
6. Run `query_with_evidence()`.
7. Run `wiki_store.lint_wiki()`.
8. Delete generated test state.

**Gate:** ingestion, graph traversal, evidence retrieval, wiki search, and linting run successfully.

### Phase 2 — Add Repository Guidance

1. Add `AGENTS.md` with the knowledge-base rules.
2. Add `README.md` explaining the three layers and primary workflows.
3. Document the required Python version and invocation examples.
4. Define whether `data/` and generated wiki indexes are committed.

Recommended policy:

- Commit `wiki/` because it is the persistent knowledge artifact.
- Commit `data/` when graph state must be shared across machines.
- Exclude only temporary smoke-test data, caches, and Python bytecode.

**Gate:** an agent can determine where new content belongs and how to query it without inspecting commit history.

### Phase 3 — Inventory Existing Documents

1. List every tracked knowledge document.
2. Classify each as active, superseded, duplicate, or uncertain.
3. Assign a lowercase kebab-case target path.
4. Assign a stable document ID.
5. Identify overlapping documents and broken links.
6. Record the result in the migration map.

**Gate:** every current document has exactly one planned destination and disposition.

### Phase 4 — Normalize Source Files

1. Create `sources/` and `archive/`.
2. Move active source documents using `git mv`.
3. Normalize filenames to lowercase kebab-case.
4. Preserve content during the move.
5. Repair repository links.
6. Move obsolete documents to `archive/` only after review.

**Gate:** no active knowledge documents remain scattered across the repository root or unrelated folders.

### Phase 5 — Ingest Sources Incrementally

Process three to five documents per batch:

1. Read `references/ingestion.md` and `references/ontology.md`.
2. Extract only entities and relations supported by the source.
3. Include `supporting_text` for every entity and relation.
4. Call `ingest_with_content(...)` with the stable document ID.
5. Create the document summary page.
6. Create or update entity pages.
7. Update relevant topic pages.
8. Run representative graph queries.
9. Run the wiki lint.

**Gate:** every ingested source exists in `data/documents.json`, has graph provenance, and has a summary page.

### Phase 6 — Build Topic Navigation

Create topic pages only after their source documents have been ingested.

Initial topics:

```text
wiki/topics/
├── agent-skills.md
├── copilot-cli.md
├── agent-workflows.md
├── context-management.md
├── agent-reliability.md
├── prompt-and-instruction-authoring.md
├── repository-search.md
└── rag-and-knowledge-retrieval.md
```

Each topic must:

- synthesize multiple sources;
- link to relevant entity and summary pages;
- distinguish facts, recommendations, and unresolved questions;
- preserve contradictory claims rather than silently choosing one.

**Gate:** each major repository theme is reachable through both wiki search and graph traversal.

### Phase 7 — Validate Graph Quality

Review:

- duplicate entities caused by aliases or casing;
- overly specific entity types;
- unsupported or weak relations;
- relations below the `0.6` confidence threshold;
- graph nodes missing provenance;
- isolated wiki pages;
- broken wikilinks;
- contradictory or stale claims;
- graph queries that return excessive noise.

Do not model every noun. Prioritize entities useful for navigation, synthesis, and retrieval.

**Gate:** graph queries return small, relevant, evidence-backed subgraphs.

### Phase 8 — Add Automation

Add a repository validation script or workflow that checks:

- Python imports compile;
- skill frontmatter is valid;
- `wiki_store.lint_wiki()` reports no unexplained issues;
- graph node and edge provenance resolves to stored documents and chunks;
- stable document IDs are unique;
- expected generated files are valid JSON;
- no temporary test data is committed.

**Gate:** structural and graph-integrity failures are detected before merge.

### Phase 9 — Archive and Deduplicate

1. Identify overlapping sources after ingestion.
2. Keep source documents immutable for provenance.
3. Mark superseded claims in wiki pages.
4. Move inactive sources to `archive/`.
5. Keep one canonical wiki synthesis per topic.
6. Never remove conflicting evidence silently.

**Gate:** active navigation exposes one canonical topic page while preserving source history.

### Phase 10 — Completeness Sweep

Verify:

- every original document was migrated, archived, or deliberately excluded;
- every active source is ingested;
- every ingested source has a summary page;
- important entities have entity pages;
- major themes have topic pages;
- every graph relation has supporting evidence;
- no broken wiki links remain;
- no unexplained orphan or isolated pages remain;
- repository instructions match the actual structure;
- representative queries return useful results.

Completion is not allowed while any document has an unknown disposition.

## Recommended Pull Requests

```text
PR 1 — Add mini-context-graph skill
PR 2 — Add repository policy and runtime documentation
PR 3 — Move documents into sources/
PR 4 — Ingest first document batch
PR 5 — Ingest remaining documents
PR 6 — Add synthesis topics and repair graph quality
PR 7 — Add smoke tests and graph integrity validation
PR 8 — Archive obsolete sources and complete migration
```

Keep structural moves separate from ingestion so file-history changes, graph-state changes, and synthesized content can be reviewed independently.

## Definition of Done

- The repository skill is installed and smoke-tested.
- All active documents live under `sources/`.
- The wiki is the default navigation surface.
- Graph traversal is used for structural and relationship queries.
- Every graph node and edge is evidence-backed.
- `wiki/` and shared `data/` state are reproducible and reviewable.
- Repository guidance defines ingestion, retrieval, lint, archive, and contradiction handling.
- No active knowledge document remains unclassified.
