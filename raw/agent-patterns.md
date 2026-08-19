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

---

# Multi-Agent Orchestration Patterns

## 1. Classify-and-Act

A classifier decides **what kind of task this is** and routes it to the appropriate specialist agent.

```text
Task → Classifier → Agent A / Agent B / Agent C
```

Example:

- Bug → Debugging agent
- Feature → Coding agent
- Documentation → Docs agent

Best for: tasks that fall into clear categories.

---

## 2. Fanout-and-Synthesize

Send the task to **multiple agents in parallel**, then combine their results.

```text
Task → Agent A ─┐
     → Agent B ─┼→ Synthesizer → Final result
     → Agent C ─┘
```

Example:

- Agent A → architecture
- Agent B → security
- Agent C → performance
- Synthesizer → combined recommendation

Best for: research, design, and broad analysis.

---

## 3. Adversarial Verification

One agent produces the work while other agents **challenge and verify it**.

```text
Worker → Verifier A
       → Verifier B
       → Verifier C
```

Example:

A coding agent implements a change while reviewers independently check:

- Correctness
- Security
- Edge cases

Best for: increasing reliability and catching mistakes.

---

## 4. Generate-and-Filter

Generate **multiple candidate solutions**, then filter or score them using explicit criteria.

```text
Generators → Candidates → Filter → Best candidates
```

Example:

Generate several API designs and evaluate them for:

- Simplicity
- Backward compatibility
- Performance
- Maintainability

Best for: large solution spaces where you want to choose the best candidate.

---

## 5. Tournament

Multiple solutions compete through **pairwise comparisons** until one wins.

```text
A vs B ─┐
        ├→ Winners → Final Judge → Winner
C vs D ─┘
```

Example:

Instead of ranking 10 architecture proposals at once:

1. Compare A vs B
2. Compare C vs D
3. Compare the winners
4. Select the final winner

Best for: situations where relative comparison is easier than absolute scoring.

---

## 6. Loop Until Done

An agent repeatedly works, evaluates progress, and continues until the stopping condition is satisfied.

```text
Agent → New findings?
          ↓ yes
        Continue
          ↓ no
         Done
```

Example:

1. Inspect service
2. Discover dependency
3. Inspect dependency
4. Discover another dependency
5. Continue until no relevant dependencies remain

Best for: exploration, debugging, implementation, and iterative problem solving.

---

## Cheat Sheet

| Pattern | Main Idea |
|---|---|
| Classify-and-Act | Route |
| Fanout-and-Synthesize | Parallelize + combine |
| Adversarial Verification | Challenge + verify |
| Generate-and-Filter | Generate many + select |
| Tournament | Compete + eliminate |
| Loop Until Done | Iterate until complete |

## Composition Example

These patterns can be combined:

```text
Classify
  ↓
Coding Agent
  ↓
Adversarial Review
  ↓
Loop Until Tests Pass
  ↓
Done
```
