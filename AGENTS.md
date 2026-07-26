# Knowledge Base Operating Rules

## Repository layers

- sources/ is the canonical, human-maintained source corpus. Source files are immutable after ingestion; corrections become new source revisions.
- wiki/ is agent-maintained synthesized knowledge. Use wiki_store.write_page() for page writes so index.md and log.md stay consistent.
- data/ is machine-managed graph, raw-document, ontology, and search-index state. Commit it with the wiki.
- .agents/skills/mini-context-graph/ is the installed mini-context-graph skill and its Python runtime.

## Ingestion rules

1. Read the installed skill references/ingestion.md and references/ontology.md before extracting knowledge.
2. Search the wiki before searching raw sources when answering questions.
3. Ingest every new source with its stable document ID and repository-relative source path.
4. Create one summary page for every ingested source.
5. Create or update relevant entity and topic pages.
6. Do not invent entities or relations. Every entity and relation must have supporting source text.
7. Use canonical ontology types and relations; reject relations with confidence below 0.6.
8. Keep graph traversal at depth 2 and no more than 50 nodes.
9. Preserve contradictions as unresolved notes; do not silently select a winning claim.

## Generated-file rules

- Never manually edit wiki/index.md or wiki/log.md.
- Run the skill's wiki_store.lint_wiki() after ingestion.
- Before committing, check source coverage, document IDs, provenance, evidence, JSON validity, and wiki links using the skill runtime directly.
- Do not commit temporary extraction JSON, caches, Python bytecode, or smoke-test directories.
- Do not delete wiki pages or source evidence without explicit human review.

## Runtime

The skill directory is configured with MINI_CONTEXT_GRAPH_SKILL_DIR. The repository-local installation is:

    .agents\skills\mini-context-graph

Document ingestion and validation are performed by an agent using the
repository-local skill directly. No GitHub Actions workflow is required.
