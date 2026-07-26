## Problem

Droid executes a long, fixed workflow. Context compaction, agent crashes, tool failures, or session interruption can lose the current execution position.

Current `Emit` messages provide observability, but they are stored only in conversation context. They do not reliably preserve:

- the current phase;
- completed steps and skill calls;
- changed files;
- verification attempts;
- skipped-step reasons;
- the exact point from which execution should resume.

The final status report also lists results, but it does not prove that every required phase was considered.

## Goal

Make Droid a resumable, auditable workflow that:

1. continues safely after compaction, interruption, or crash;
2. never silently omits a required phase;
3. records which skills and steps ran;
4. records why any step or skill did not run;
5. validates completeness before reporting completion.

## Proposed design

Treat Droid as a durable state machine rather than only a sequence of prompt sections.

```text
initialize/resume
    ↓
input
    ↓
preflight
    ↓
exploration
    ↓
guardrails
    ↓
implementation
    ↓
feedback
    ↓
problem logging
    ↓
finalization / completeness sweep
```

Each phase must define:

```text
preconditions
start checkpoint
execution
postconditions
completion checkpoint
outcome + reason
```

### 1. Add invocation-scoped durable state

Create:

```text
.droid/runs/<RUN_ID>/state.json
.droid/runs/<RUN_ID>/events.jsonl
```

- `state.json`: atomically replaced snapshot of the current run.
- `events.jsonl`: append-only audit trail.
- `RUN_ID`: unique per invocation, for example `20260725T142201Z-a18f3c`.

Example state:

```json
{
  "schemaVersion": 1,
  "runId": "20260725T142201Z-a18f3c",
  "taskFingerprint": "sha256:...",
  "status": "running",
  "currentPhase": "feedback",
  "resumeFrom": "feedback.verify",
  "phases": {
    "input": { "status": "completed", "reason": "Harness paths resolved" },
    "preflight": { "status": "completed", "reason": "Build passed; LSP unavailable" },
    "exploration": { "status": "completed", "reason": "Relevant files inspected" },
    "guardrails": { "status": "completed", "skill": "droid-memory" },
    "implementation": { "status": "completed", "skill": "droid-implement" },
    "feedback": {
      "status": "in_progress",
      "skill": "droid-feedback",
      "resumeFrom": "tests",
      "attempt": 2
    },
    "problem_logging": { "status": "not_started" },
    "finalization": { "status": "not_started" }
  },
  "changedFiles": ["src/Foo.cs", "tests/FooTests.cs"]
}
```

Conversation messages explain progress; filesystem state determines progress.

### 2. Initialize state before other work

The first durable action must be:

```text
resolve or create RUN_ID
create or resume run state
persist task fingerprint
then resolve harness paths and execute commands
```

This ensures failures during input, preflight, or exploration still leave a continuation point.

### 3. Add task identity and stale-run protection

Calculate a task fingerprint from:

- normalized task text;
- workspace path;
- starting Git commit;
- issue URL or plan identifier, when present.

Resume automatically only when the fingerprint matches an unfinished run.

When it does not match:

- do not reuse the old run;
- create a new `RUN_ID`;
- report the unfinished prior run.

### 4. Use explicit phase outcomes

Allowed states:

```text
not_started
in_progress
completed
skipped
not_applicable
blocked
partial
failed
```

Every phase not marked `completed` must include a reason.

Do not use an ambiguous `not called` state. It must be clear whether a phase was skipped intentionally, not applicable, blocked by a prerequisite, not reached, or failed.

### 5. Checkpoint every skill call

Before invoking a skill:

```json
{"event":"skill_call_started","skill":"droid-memory","phase":"guardrails"}
```

After invocation:

```json
{"event":"skill_call_finished","skill":"droid-memory","outcome":"completed"}
```

On failure:

```json
{
  "event": "skill_call_finished",
  "skill": "droid-feedback",
  "outcome": "blocked",
  "reason": "NuGet authentication failed"
}
```

The final report must derive its called/not-called ledger from these durable events rather than conversation history.

### 6. Define resume behavior

At startup:

1. Find the latest matching non-terminal run.
2. Read `state.json` and `events.jsonl`.
3. Validate artifacts for phases marked completed.
4. Resume the first incomplete or invalid phase.

Rules:

- Completed phase with valid artifacts → skip execution and record that it was resumed as already complete.
- Completed phase with invalid or missing artifacts → mark stale and rerun.
- `in_progress` phase with satisfied postconditions → record recovered completion.
- `in_progress` phase without satisfied postconditions → restart from that phase's safe boundary.
- Terminal run → create a new run unless the user explicitly requests inspection.

Prefer phase-level restart over resuming after an arbitrary command.

Safe restart boundaries:

```text
input
preflight
exploration
guardrails
implementation
feedback.verify
feedback.refactoring-review
problem-logging
finalization
```

### 7. Make phases idempotent

Every phase must be safe to rerun.

Examples:

- path resolution must not duplicate configuration;
- implementation must inspect the current diff before editing;
- verification can run repeatedly;
- log entries must use `runId + problemId` for deduplication;
- completion events must not be duplicated.

Add to problem-log entries:

```md
- **run-id**: <RUN_ID>
- **problem-id**: <stable identifier>
```

### 8. Always execute finalization

Replace immediate termination semantics with finally-style behavior:

```text
If blocked, stop normal phase execution, persist the blocker,
run problem logging when possible, and always run finalization.
```

This also resolves the current inconsistency where `droid-log` can record feedback blockers, but the agent reaches problem logging only after feedback passes.

### 9. Add phase postconditions

| Phase | Required completion evidence |
|---|---|
| Input | All paths resolved or explicitly missing |
| Preflight | Build and LSP results persisted |
| Exploration | Explored files and conventions recorded |
| Guardrails | Memory-read outcome recorded |
| Implementation | Diff exists or explicit no-change reason |
| Feedback | Verification receipts and retry counts recorded |
| Problem logging | Logged count or explicit zero result |
| Finalization | Terminal status and complete phase ledger written |

A phase must not be marked completed before its evidence is validated.

### 10. Persist verification receipts

For each verification command, store:

```json
{
  "command": "dotnet test Foo.sln",
  "exitCode": 0,
  "startedAt": "...",
  "finishedAt": "...",
  "outputPath": ".droid/runs/<RUN_ID>/logs/test-2.log",
  "gitDiffHash": "sha256:..."
}
```

Verification must correspond to the final diff. A result for an earlier diff does not prove that the final code passed.

### 11. Add a mandatory completeness sweep

Before returning `STATUS: complete`:

1. Enumerate every defined phase.
2. Verify each phase has a terminal outcome.
3. Validate evidence for every completed phase.
4. Verify every configured skill is classified as called or not called.
5. Require a reason for every skipped, blocked, failed, partial, not-applicable, or not-reached phase.
6. Confirm verification receipts match the final diff.
7. Persist the terminal state before generating the user report.

Completion is forbidden when any phase remains `not_started` or `in_progress`.

### 12. Improve the final status report

```text
STATUS: complete | blocked | partial | failed
RUN ID: <id>
RESUMED: yes | no
SUMMARY: <technical result>
FILES: <changed files>

WORKFLOW:
- INPUT: completed — harness settings resolved
- PREFLIGHT: completed — build passed; LSP unavailable
- EXPLORATION: completed — inspected 6 files
- GUARDRAILS: completed — called droid-memory
- IMPLEMENTATION: completed — called droid-implement
- FEEDBACK: blocked — called droid-feedback; SDK unavailable
- PROBLEM LOGGING: completed — called droid-log; one blocker recorded
- FINALIZATION: completed — completeness sweep passed

SKILLS CALLED:
- droid-memory — required guardrail loading
- droid-implement — implementation rules required
- droid-feedback — verification required
- droid-log — blocker required durable logging

SKILLS NOT CALLED:
- <skill> — skipped | not applicable | blocked by prerequisite | not reached
  Reason: <specific reason>

VERIFICATION:
- Build: pass
- Tests: blocked — SDK unavailable
- Refactoring review: not reached because tests were blocked

RESUME:
- Exact phase: feedback.verify
- Next action: install the required SDK and rerun Droid
```

### 13. Keep the orchestrator thin

Keep only these concerns in `droid.agent.md`:

- phase order;
- state-machine rules;
- mandatory gates;
- terminal-report contract;
- links to detailed protocols.

Move persistence and recovery logic into a reusable skill and deterministic script:

```text
plugins/droid/
├── agents/droid.agent.md
└── skills/droid-run-state/
    ├── SKILL.md
    ├── references/state-schema.md
    └── scripts/droid-state.py
```

Suggested commands:

```bash
droid-state.py init
droid-state.py resume
droid-state.py phase-start exploration
droid-state.py phase-end exploration completed
droid-state.py skill-start droid-memory
droid-state.py skill-end droid-memory completed
droid-state.py block feedback "SDK unavailable"
droid-state.py report
```

Use a script for atomic writes, schema validation, deduplication, and report generation instead of repeatedly asking the model to edit JSON manually.

### 14. Fix documentation drift

Update `plugins/droid/README.md` to match the current agent phases. Add a repository check that validates the documented phase sequence against `droid.agent.md`.

## Implementation priority

1. Durable state, run ID, and task fingerprint.
2. Resume semantics with artifact validation.
3. Explicit phase and skill outcome ledger.
4. Always-run finalization and completeness sweep.
5. Idempotent writes and verification receipts.
6. Thin orchestrator plus scripted state management.
7. README consistency validation.

## Acceptance criteria

- [ ] An interrupted run can resume from the first incomplete safe phase.
- [ ] Compaction does not lose phase or skill-call state.
- [ ] Each phase has an explicit outcome and reason.
- [ ] Every skill is reported as called or not called with a reason.
- [ ] `STATUS: complete` is impossible while any phase is unfinished.
- [ ] Completed phases are validated using durable evidence.
- [ ] Verification receipts correspond to the final diff.
- [ ] Problem logging runs for blocked feedback executions when possible.
- [ ] Re-running a phase does not duplicate state or problem-log entries.
- [ ] The final report includes `RUN ID`, resume point, workflow ledger, skill ledger, and verification status.
- [ ] Droid README and agent workflow definitions remain synchronized.
