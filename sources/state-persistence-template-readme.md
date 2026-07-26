# Claude Agent Template Pack

This pack is designed to make Claude-style coding workflows retry-safe.

## Included Files
- `CLAUDE.md` — persistent rules and invariants
- `TASKS.md` — atomic task tracker
- `PROGRESS.md` — working memory / checkpoint
- `.claude/handoff.md` — restart instructions
- `.claude/failures.md` — anti-doom-loop memory
- `.claude/results/ST-001.md` — example completed task output

## Recommended Workflow
1. Read all state files at the start of each attempt.
2. Work on one atomic task.
3. Verify.
4. Checkpoint progress.
5. Write learnings before ending or retrying.
