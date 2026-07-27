# AI Steering Best Practices

## What Is Steering?

**Steering** means guiding or directing something toward a desired outcome.

In AI / Copilot context, **steering** means giving the model instructions, constraints, examples, and feedback so it behaves the way you want.

In simple words:

> Steering = controlling the direction of the AI response without directly coding everything yourself.

## Basic Example

```text
Generate a PRD, but keep it short, bullet-only, implementation-focused, and under 250 words.
```

This steers the AI toward:

```text
short + structured + useful for implementation
```

## Common Steering Methods

| Steering method | Example |
| --- | --- |
| Role | You are a senior .NET architect. |
| Goal | Create a vertical-slice implementation plan. |
| Constraints | No generic text. Max 300 words. |
| Format | Output as AsciiDoc. |
| Examples | Follow this example style. |
| Feedback | Make it shorter and more technical. |

## Practical Prompt Pattern

Use this structure when you want predictable AI output:

```text
Role: <who the AI should act as>
Goal: <what result you want>
Context: <important background only>
Constraints: <hard rules and limits>
Output: <required format>
Examples: <optional example to copy>
```

## Example: Steering Copilot for Implementation Planning

```text
Role: You are a senior software architect.
Goal: Generate an implementation plan from the PRD and GitHub issues.
Context: Use the provided PRD and issue list as the source of truth.
Constraints:
- Preserve dependencies between issues.
- Prefer vertical slices.
- Keep batches safe for autonomous execution.
- Include rollback strategy.
Output:
- Dependency graph
- Execution order
- Vertical slices
- Autonomous execution batches
- Rollback strategy
```

## Why Steering Matters

Good steering helps the AI avoid:

- Too much generic explanation
- Missing important constraints
- Wrong output format
- Over-engineered answers
- Losing implementation context

Good steering improves:

- Predictability
- Review speed
- Implementation quality
- Agentic execution safety
- Reuse of prompts across tasks

## TL;DR

- Steering is how you guide AI behavior.
- Use role + goal + context + constraints + output format.
- Strong constraints are better than asking for “short text”.
- Examples are powerful because the AI can copy the desired shape.
- Feedback is also steering: each correction narrows the next answer.
