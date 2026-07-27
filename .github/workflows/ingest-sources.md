---
name: Update Graphify knowledge graph
on:
  push:
    branches: [main]
    paths:
      - raw/**
engine: copilot
permissions:
  contents: read
concurrency:
  group: graphify-ingestion
  cancel-in-progress: false
safe-outputs:
  create-pull-request:
    max: 1
    title-prefix: "[graphify] "
    labels:
      - graphify
    base-branch: main
    allowed-branches:
      - automated-ingest/*
    preserve-branch-name: true
    recreate-ref: true
    draft: false
    fallback-as-issue: false
    github-token-for-extra-empty-commit: ${{ secrets.GH_AW_CI_TRIGGER_TOKEN }}
    allowed-files:
      - graphify-out/**
pre-agent-steps:
  - name: Install Graphify CLI
    shell: bash
    run: |
      graphify_venv="${RUNNER_TEMP}/graphify-venv"
      python3 -m venv "$graphify_venv"
      "$graphify_venv/bin/python" -m pip install --disable-pip-version-check --no-cache-dir graphifyy==0.9.27
      echo "$graphify_venv/bin" >> "$GITHUB_PATH"
      "$graphify_venv/bin/graphify" --help >/dev/null
---

# Update the Graphify knowledge graph

Keep the repository's Graphify output synchronized when files under `raw/`
change. This workflow is triggered after a push to `main` that changes the raw
corpus.

## Rules

- Read `AGENTS.md` and `.copilot/skills/graphify/SKILL.md` first.
- Treat every file under `raw/` as immutable. Never edit, delete, or rewrite it.
- Use the existing workflow environment variables for Graphify's configured
  backend. Never print credentials or create new secrets in the workflow.
- Do not add temporary extraction files, caches, bytecode, or test directories.

## Update

1. Determine the changed files under `raw/` from the push event.
2. If no supported raw file remains, finish without requesting a PR.
3. Set `GRAPHIFY_OUT=graphify-out` and invoke the Graphify skill against `raw/`
   with incremental update and wiki generation: `/graphify raw --update --wiki`.
   If a headless CLI is required, use `graphify extract raw --out .` with the
   configured backend.
4. Validate `graphify-out/graph.json` as JSON and verify generated source paths
   stay under `raw/`.
5. Request exactly one non-draft PR using the `create_pull_request` safe output.
   Use the stable branch name `automated-ingest/graphify`, target `main`, and
   include changed raw paths and validation results in the PR body.

The workflow must never request a PR that changes `raw/`, repository
instructions, project skills, or workflow files.
