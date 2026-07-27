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

Headless CLI equivalent (used by CI, also runnable manually from Codex,
Copilot, or a plain terminal — no agent orchestration required):

```bash
export GRAPHIFY_OUT=graphify-out
export OPENAI_API_KEY=sk-proj-...   # required for semantic extraction
graphify extract raw --out . --backend openai
```

Run that command from the repository root. On PowerShell, set the output path
explicitly before running it:

```powershell
$env:GRAPHIFY_OUT = (Join-Path (Get-Location) 'graphify-out')
graphify extract raw --out . --backend openai
```

Do not use the shell command form `graphify raw ...` for this repository; it
can resolve generated state relative to `raw/` and create `raw/graphify-out/`.

Extraction has two paths: structural (AST) extraction for code needs no LLM
or API key; semantic extraction for docs/PDFs/images calls the `--backend`
LLM and requires its API key. Since `raw/` is all Markdown, `OPENAI_API_KEY`
is effectively required for this command to do anything.

Supported `--backend` values: `openai`, `gemini`, `kimi`, `deepseek`,
`claude-cli`. Each requires its own API key/credentials except `claude-cli`,
which uses a local Claude CLI login. This repository standardizes on
`openai`.

## GitHub Actions secrets

The ingestion pipeline requires this repository secret:

- `OPENAI_API_KEY` — an OpenAI project API key (`sk-proj-...`) used by
  `graphify extract` for semantic document extraction.

`GH_AW_CI_TRIGGER_TOKEN` is optional. If configured, it allows the generated
pull request's validation and auto-merge workflows to run without manual
approval; otherwise the pipeline falls back to `GITHUB_TOKEN`.

## Supported ingestion file types

The Graphify pipeline supports:

- Documentation: `.md`, `.mdx`, `.qmd`, `.html`, `.txt`, `.rst`, `.yaml`, `.yml`
- Code and configuration: Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, C#, Ruby, Kotlin, Scala, PHP, Swift, Lua, Vue, Svelte, Astro, Groovy, Dart, SQL, shell, JSON, Terraform/HCL, Pascal, and project manifests
- Office files: `.docx`, `.xlsx`
- PDFs: `.pdf`
- Images: `.png`, `.jpg`, `.webp`, `.gif`
- Video and audio: `.mp4`, `.mov`, `.mp3`, `.wav`

`.adoc` and `.asciidoc` are not natively detected by the current headless
pipeline and must be converted to a supported text format before ingestion.

Graphify output is generated and reviewable. Do not edit `raw/` during graph
generation, and do not commit `graphify-out/cache/` or `graphify-out/cost.json`.

Do commit `graphify-out/manifest.json` — it records per-file hashes/timestamps
so a later `--update` run can detect what changed and re-extract only that
subset instead of the whole corpus.
