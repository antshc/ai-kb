# Copilot PRD Compression Best Practices (TL;DR Style)

## Key Instruction Phrases

Use strong, unambiguous phrases:

- `compressed PRD`
- `high-density PRD`
- `zero-fluff PRD`
- `bullet-only PRD`
- `implementation-focused PRD`
- `review-in-2-minutes PRD`


## Purpose

Define a consistent way to instruct Copilot to generate minimal, high-density PRDs that:

- Preserve full implementation context
- Are fast to review (≤ 2 minutes)
- Can be directly broken into development tasks


## Core Principle

Do not ask for "short text".

Instead, enforce:

- Compression
- Structure
- Constraints

Copilot responds better to:

- Clear formats
- Hard limits
- Explicit rules

### Recommended Combination

Generate a compressed, high-density, bullet-only PRD.

## Mandatory Constraints

Always include strict rules:

- Bullet points only (no paragraphs)
- Max 250 words total
- Max 5–8 bullets per section
- No repetition
- No generic statements
- Only implementation-relevant information

Without constraints, Copilot will produce verbose output.

## Standard TL;DR PRD Template

```asciidoc
= PRD (TL;DR)

== Problem (max 3 bullets)

* What problem are we solving?
* Who is affected?
* Why now?

== Goal (max 3 bullets)

* Measurable outcome
* Success criteria

== Scope

=== In Scope

* ...

=== Out of Scope

* ...

== Functional Requirements (max 8 bullets)

* System must ...

== Edge Cases (max 5 bullets)

* If X fails → Y

== Technical Notes (max 5 bullets)

* Integrations
* Constraints
* Performance assumptions

== Risks (max 3 bullets)

* ...

== TL;DR (1–2 lines)

Short summary
```

## Quality Rules

Each bullet must:

- Contain subject + action
- Include condition if relevant
- Be testable

### Example

Bad:

- Handle errors

Good:

- System must return "Availability Unknown" if external API fails

## Anti-Hallucination Rule

Always include:

If information is missing:

- Do NOT invent
- Mark as `TBD`

## Task Breakdown Readiness

Ensure requirements are:

- Independent
- Small
- Implementable as vertical slices

## Compression Enforcement

Optional but recommended:

```text
Total document must not exceed 200–300 words
```

## Full Prompt (Copy-Paste)

```text
Generate a compressed, high-density, implementation-focused PRD.

Compress wording, not meaning.

Preserve:
- architectural decisions
- integration constraints
- edge cases
- operational behavior
- business invariants
- assumptions required for implementation

Remove:
- filler
- explanations
- marketing wording
- repetition
- generic statements

Use:
- bullet points only
- short technical statements
- implementation-oriented language
- explicit behavior rules
```
