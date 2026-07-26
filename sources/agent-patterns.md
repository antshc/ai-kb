# Agent Patterns

## Pattern #1 — Sequential Flow

Agents run one after another.

Each step depends on the output of the previous step.

```text
Input → Agent A → Agent B → Agent C → Output
```

Use when the task has clear stages.

Example:

```text
Research → Plan → Implement → Review
```

Good for:

- deterministic workflows
- step-by-step processing
- reducing chaos
- enforcing order

Risk:

- slow, because agents wait for each other
- bad output early can poison the whole chain

---

## Pattern #2 — The Operator

One central agent controls the workflow.

The operator decides:

- what to do next
- which tool or agent to call
- when to stop
- how to combine results

```text
User → Operator Agent → Tools / Subagents → Final Output
```

Use when the task needs coordination and decisions.

Example:

```text
Operator reads GitHub issue
→ calls research agent
→ calls coding agent
→ calls test agent
→ summarizes result
```

Good for:

- dynamic workflows
- uncertain tasks
- tasks with branching decisions
- agent orchestration

Risk:

- operator can become overloaded
- bad routing decisions affect everything

---

## Pattern #3 — Split & Merge

The task is split into independent parts.

Multiple agents work in parallel.

Then results are merged.

```text
Input
 ├─ Agent A
 ├─ Agent B
 └─ Agent C
      ↓
   Merge Agent → Output
```

Use when parts can be processed independently.

Example:

```text
Review backend code
Review frontend code
Review database migration
→ merge findings into one review
```

Good for:

- faster execution
- parallel analysis
- large tasks
- independent subtasks

Risk:

- duplicated work
- inconsistent assumptions
- merge step can miss conflicts

---

## Pattern #4 — Agent Teams

Multiple agents have specialized roles.

They collaborate like a small team.

```text
Planner Agent
Coder Agent
Reviewer Agent
Tester Agent
Architect Agent
```

Each agent owns one responsibility.

Example:

```text
Architect designs solution
Coder implements
Tester writes tests
Reviewer checks risks
```

Good for:

- complex engineering tasks
- specialized reasoning
- higher-quality review
- separating responsibilities

Risk:

- coordination overhead
- agents may disagree
- more tokens and time
- needs clear contracts between agents

---

## Pattern #5 — Headless

Agents run without direct user interaction.

Usually triggered by script, CLI, CI job, scheduler, or background automation.

```text
Trigger → Agent Workflow → Commit / Report / Issue Update
```

Use when the process should run automatically.

Example:

```text
CI failure detected
→ agent analyzes logs
→ creates fix branch
→ opens PR
```

Good for:

- automation
- repetitive tasks
- GitHub issue processing
- CI/CD workflows
- AFK coding agents

Risk:

- unsafe without guardrails
- may change too much
- needs logging, limits, rollback
- should avoid destructive actions unless explicitly allowed
