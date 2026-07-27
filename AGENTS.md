# Knowledge Base Operating Rules

## Repository layers

- `raw/` is the canonical, human-maintained source corpus. Keep it immutable; corrections become new source revisions.
- `graphify-out/` is the generated Graphify knowledge layer. Commit the graph, report, visualization, and wiki; do not manually edit them.
- `.codex/` and `.copilot/` contain project-scoped Graphify integrations.

## Graphify workflow

1. For knowledge-base questions, query the existing graph before reading the raw corpus:
   `graphify query "<question>"`.
2. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts.
3. Use `graphify-out/wiki/index.md` for broad navigation when it exists.
4. Local ingestion is user-triggered only. Do not run Graphify automatically
   after edits, commits, or file changes. When the user explicitly requests a
   local refresh, set `GRAPHIFY_OUT=graphify-out` and invoke
   `/graphify raw --update --wiki`; for headless CLI use
   `graphify extract raw --out .` with the configured backend. GitHub Actions
   performs automatic ingestion after a push to `main` changes `raw/**`.
5. Never modify files under `raw/` during extraction or graph maintenance.

## Generated-file rules

- Commit only intentional Graphify output changes under `graphify-out/`.
- Do not commit Graphify cache, local cost metadata, temporary files, or Python bytecode.
- Validate graph JSON and source-file paths before committing.

## Project integrations

- Codex: `.codex/skills/graphify/`.
- GitHub Copilot: `.copilot/skills/graphify/`.
