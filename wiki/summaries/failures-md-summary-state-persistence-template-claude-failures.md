---
title: failures.md Summary (state-persistence-template-claude-failures)
source_document: source-state-persistence-template-claude-failures
tags: [summary]
---

# failures.md

**Source:** `sources/state-persistence-template-claude-failures.md`

## Summary

Track failed attempts so retries do not repeat the same bad reasoning. **What failed** - **Root cause** - **Do not retry** - **Correct next action** - --- **What failed** - Checked free disk space on every cache write. **Root cause** - Added too much overhead to hot IO path. **Do

## Entity

- [[failures-md]] (concept)
