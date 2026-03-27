# handoff.md

## If a new Claude session starts, do this first:
1. Read `CLAUDE.md`
2. Read `TASKS.md`
3. Read `PROGRESS.md`
4. Read `.claude/failures.md`
5. Read any relevant files in `.claude/results/`

## Resume Rule
Continue only the next incomplete atomic task.

## Before making changes
- Confirm the task is not already complete.
- Confirm prior failed approaches are not being repeated.

## Before ending session
Update:
- `TASKS.md`
- `PROGRESS.md`
- `.claude/failures.md` (if anything failed)
- `.claude/results/<TASK-ID>.md` (if task completed)
