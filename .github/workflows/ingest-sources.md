---
name: Ingest knowledge sources
on:
  push:
    branches: [main]
    paths:
      - sources/**
engine: copilot
permissions:
  contents: read
safe-outputs:
  create-pull-request:
    max: 1
    title-prefix: "[automated-ingest] "
    labels:
      - automated-ingest
    allowed-files:
      - wiki/**
      - data/**
---

# Automatic source ingestion

Ingest all supported source files changed by this push into the repository's
mini-context-graph knowledge base. This workflow is triggered only after a
push to `main` that changes `sources/**`.

## Required repository rules

Read `AGENTS.md` and these files before processing any source:

- `.agents/skills/mini-context-graph/references/ingestion.md`
- `.agents/skills/mini-context-graph/references/ontology.md`
- `.agents/skills/mini-context-graph/references/lint.md`
- `.agents/skills/mini-context-graph/scripts/contextgraph.py`
- `.agents/skills/mini-context-graph/scripts/tools/wiki_store.py`

The source corpus is immutable. Never edit, delete, or rewrite anything under
`sources/`. Do not manually edit `wiki/index.md` or `wiki/log.md`; all wiki
pages must be written through `wiki_store.write_page()`.

## Determine the batch

Use the push's before and after revisions from the GitHub event to list changed
files. For the initial push, use the files in `sources/` at the checked-out
revision. Process every changed file directly under `sources/` whose extension
is one of `.md`, `.adoc`, `.txt`, `.rst`, `.yaml`, `.yml`, `.json`, `.csv`, or a
recognized source-code extension. Ignore deleted files, nested directories,
unsupported files, and binary files; report ignored files in the run summary.

If no supported source remains, finish without requesting a PR.

## Ingest each source

Process the complete batch in one run. For every source file:

1. Read the full UTF-8 content.
2. Compute a SHA-256 hash of the content. Use a stable document ID made from
   the normalized repository-relative path and the first 16 characters of the
   hash, for example `sources/example-md-0123456789abcdef`.
3. Extract entities and relations according to `ingestion.md` and normalize
   types and relations according to `ontology.md`.
4. Include verbatim or near-verbatim `supporting_text` for every entity and
   relation. Reject relations below confidence `0.6`.
5. Call `ContextGraphSkill.ingest_with_content()` with the document ID, source
   path, title, complete raw content, entities, and relations.
6. Write one summary page for the document with `wiki_store.write_page()`.
7. Create or update entity pages with `wiki_store.write_page()`, preserving
   contradictions as unresolved notes and adding source-summary links.
8. Do not invent entities, relations, claims, or sources.

Use the repository-local Python runtime and set the skill scripts on
`PYTHONPATH`. Do not add temporary extraction files, caches, bytecode, or test
directories to the working tree.

## Validation gate

Before requesting a PR:

- Run `wiki_store.lint_wiki()` and fail on orphan, missing, or broken-link
  issues.
- Validate every JSON file in `data/`.
- Verify every changed source has a corresponding document ID and stored raw
  content with the correct source path and content hash.
- Verify graph nodes and edges created by this batch have source-document
  provenance and supporting evidence.
- Verify only `wiki/**` and `data/**` have changed.
- Do not request a PR if any validation fails; report the failure clearly.

## Pull request

When the batch succeeds and generated changes exist, request exactly one PR
through the `create-pull-request` safe output. Use a deterministic branch name
`automated-ingest/${{ github.run_id }}` and a title describing the number of
ingested documents. Include in the PR body:

- changed source paths;
- document IDs and chunk counts;
- nodes and edges added;
- validation results;
- ignored files, if any.

The PR may contain only generated `wiki/` and `data/` changes. Never request a
PR that changes `sources/`, `AGENTS.md`, workflow files, or skill files.
