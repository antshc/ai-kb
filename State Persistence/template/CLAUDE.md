# CLAUDE.md

## Purpose
This file contains persistent project rules and engineering constraints for Claude-style coding agents.

## Project Invariants
- Preserve existing architecture boundaries.
- Prefer small, reviewable changes.
- Do not silently change public contracts.
- Keep retries idempotent.

## Coding Rules
- Always read `TASKS.md` and `PROGRESS.md` before making changes.
- Before editing, check whether the task is already done.
- After every meaningful milestone, checkpoint progress.
- Record rejected approaches to avoid retry loops.
- Prefer incremental commits / atomic changes.

## Retry Rules
- Never assume previous context is still available.
- Restore state from files first.
- If a prior attempt failed, read `.claude/failures.md` before retrying.
- If a subtask is complete, write a result file under `.claude/results/`.

## Verification Rules
Before marking a task DONE, run:
- build
- tests
- lint / formatting
- smoke validation (if relevant)

## Output Rules
Every completed task should leave behind:
- What changed
- Why it changed
- What failed
- What to do next
