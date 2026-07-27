# Graphify Installation and Configuration Lessons

This document distills the Codex project sessions that migrated the repository from mini-context-graph to Graphify and repaired local and CI ingestion. It is based on conversation history, not on generated graph data.

## Durable architecture

- `raw/` is the immutable, human-maintained corpus. Source corrections are new revisions; ingestion must not edit it.
- `graphify-out/` is the generated layer: `graph.json`, `GRAPH_REPORT.md`, `graph.html`, wiki, and the committed `manifest.json`.
- Do not commit caches, cost data, temporary `.graphify_*` files, reflections, or `.graphify_labels.json`.
- Keep Codex and Copilot project integrations synchronized. Fixing only one copy leaves platform-dependent failures.

## Installation

- Pin the tested package version in automation (`graphifyy==0.9.27` was used in the sessions). Avoid silently mixing package versions with project skills.
- On Windows, PyPI access stalled over IPv6. Forcing Python/pip to use IPv4 while retaining the normal hostname resolved installation; direct-IP URLs failed TLS/HTTP routing.
- Installing with `pipx` is not enough if its Scripts directory is absent from `PATH`. Persist the directory in the user `PATH` and restart the terminal.
- Verify both commands after installation: `graphify` and `graphify-mcp`.

## Command and path rules

- Distinguish the assistant workflow from the headless CLI:
  - Assistant-driven semantic extraction: `/graphify raw --update --wiki` (or the equivalent Codex skill command).
  - Headless extraction: `graphify extract ...`; it needs a supported provider/backend.
- Do not use the shell form `graphify raw ...` in this repository. It previously resolved generated state under `raw/graphify-out/`.
- The source-path validation incident showed that scanning `raw/` directly can emit basenames such as `file.md`. The validated repository-root approach was `graphify extract . --out .` with `.graphifyignore` excluding everything except the intended corpus, preserving `raw/file.md` provenance. Whichever command is retained, validate `source_file` paths and keep the same command in README, skills, and CI.
- Set `GRAPHIFY_OUT` explicitly to the repository-level `graphify-out/` before export.
- Never combine `GRAPHIFY_OUT` with another output argument or cache root; this created `graphify-out/graphify-out/cache/`.

## Cache and incremental state

- Keep source anchoring and cache location separate. The failed configuration passed `cache_root=raw`; the fix used `root=raw` with `cache_root=.` so cache landed in `graphify-out/cache`.
- Pass the explicit project cache root to semantic cache read/write calls as well as AST extraction; fixing only AST extraction leaves the same bug in semantic extraction.
- `manifest.json` is useful only when the pipeline actually preserves it and runs incremental extraction. A fresh CI runner or cleanup of all state causes full re-ingestion.
- Commit `graphify-out/manifest.json`; do not commit semantic cache or local cost metadata.
- Expected incremental behavior: unchanged files are reused, changed/new files are extracted, and deleted files are pruned during a complete refresh.

## Authentication and model selection

- `COPILOT_GITHUB_TOKEN` authenticates the Copilot agent. It is not a Graphify provider key and must not be mapped to `OPENAI_API_KEY`.
- Headless extraction needs a supported backend credential, for example:
  - OpenAI: `OPENAI_API_KEY`, `--backend openai`
  - Gemini: `GEMINI_API_KEY` or `GOOGLE_API_KEY`, `--backend gemini`
  - Claude: `ANTHROPIC_API_KEY`, `--backend claude`
  - Other documented options include DeepSeek, Moonshot/Kimi, Azure OpenAI, Bedrock, Ollama, and Claude CLI.
- Local assistant extraction can use the current Copilot/Codex session without a separate provider key. It is more complex for CI because the assistant must explicitly read and extract documents before Graphify builds the graph.
- The Copilot ingestion sessions used `claude-sonnet-4.6` with medium effort. The run exceeded ten minutes, but completed after resuming cached semantic chunks. Smaller chunks and resumability are essential for document-heavy corpora.
- Choose one architecture per pipeline: assistant/Copilot semantic extraction or headless provider-backed extraction. Mixing them caused authentication confusion and duplicate work.

## File-type coverage

- The installed Graphify detector processed Markdown but skipped the repository's `.adoc` files. Earlier mini-context-graph behavior supported `.adoc`, so do not assume support transfers during migration.
- Check supported extensions against the installed version, not only documentation. If `.adoc` must be included, explicitly convert or extract it while preserving the original `source_file: raw/...` provenance.
- Treat unsupported or skipped files as a validation failure when complete corpus coverage is required.

## CI, PR, and Pages lessons

- Keep ingestion PR-based and deterministic: stable branch, serialized runs, restricted generated paths, and validation before merge.
- Validate at minimum: non-empty `nodes`/`links`, JSON structure, every `source_file` under `raw/`, source-file existence, report/HTML/wiki presence, duplicate IDs, and non-empty HTML legend.
- `graph.html` is a committed generated artifact. A graph-only update without regenerating HTML leaves Pages stale.
- A merge performed by `github-actions[bot]` with `GITHUB_TOKEN` can suppress downstream workflow triggers. Explicitly dispatch `deploy-pages.yml` after a successful merge, or use a token with the required event permissions.
- Pages must use **GitHub Actions** as its source. Publish only a temporary `index.html` copied from `graphify-out/graph.html`.
- A successful graph can still render an empty Communities panel when HTML is exported without labels. Treat `const LEGEND = [];` as a deployment failure, not as an acceptable empty graph.
- `GH_AW_CI_TRIGGER_TOKEN` is optional for extraction; it helps agent-created PRs trigger follow-up validation/merge workflows without GitHub-token restrictions. Repository auto-merge, required checks, and Pages settings still require user configuration.

## Operational checklist

1. Install and pin Graphify; verify `graphify --version`, `graphify`, and `graphify-mcp`.
2. Set one explicit output root: repository `graphify-out/`.
3. Run the canonical extraction command from the repository root.
4. Inspect skipped extensions, cache location, manifest paths, and `source_file` provenance.
5. Validate graph, report, HTML, wiki, IDs, labels, and raw-corpus immutability.
6. Commit only intentional generated outputs plus `manifest.json`.
7. For CI, configure the provider secret or implement explicit Copilot extraction; do not rely on `COPILOT_GITHUB_TOKEN` as a provider key.
8. After merge, verify that Pages was dispatched and that the deployed HTML contains a populated legend.

## Session-derived failure patterns

| Failure | Root cause | Durable prevention |
|---|---|---|
| `pipx install graphifyy` hung | IPv6 package-index path stalled | Force IPv4 resolution; keep the normal PyPI hostname |
| `raw/graphify-out/cache` appeared | Shell command/output root resolved relative to `raw/` | Use the repository-root CLI form and explicit `GRAPHIFY_OUT` |
| `graphify-out/graphify-out/cache` appeared | Output root was applied twice | Use one output root and explicit `cache_root=.` |
| CI reported no LLM key | Copilot token was confused with a Graphify provider key | Configure `OPENAI_API_KEY`/another supported backend or extract with Copilot itself |
| Source-path validation failed | Scanning `raw/` emitted basenames | Scan the repo root with `.graphifyignore`, then validate `raw/...` paths |
| `.adoc` files were absent | Current detector did not classify `.adoc` | Add explicit `.adoc` handling and coverage checks |
| Communities panel was empty | HTML legend was empty or labels were not passed | Validate labels/legend before publishing |
| Pages did not redeploy after merge | Downstream event was suppressed for bot-created merge | Explicitly dispatch Pages or use an appropriate PAT |

