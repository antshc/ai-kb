# Concept: Lines of Inquiry → Probes → Coverage Checklist

Source: `grill-design` skill. This is the interview-structuring pattern it uses. It turns
"have a thorough discussion" into something checkable and repeatable. Three nested concepts:

## 1. Lines of inquiry

The **top-level branches** the interview must walk. Each line of inquiry is a distinct
*concern* the skill exists to interrogate (in `grill-design`: Glossary, Architecture, Testing
strategy). Rules that make this concept work:

- They are **exhaustive** for the skill's purpose — skipping one means the interview is
  incomplete, not just shorter.
- They are **not sequential steps** — the interview jumps between them as the conversation
  naturally branches, driven by what the user says, not by running them top-to-bottom as a
  batch.
- Each line of inquiry typically maps to **one output artifact** it feeds (Glossary →
  `CONTEXT.md`, Architecture → `ARCHITECTURE.md`/SSR/ADR, Testing → the testing-strategy SSR).

## 2. Probes

The **individual moves** within a line of inquiry — the actual technique the agent uses to
surface a gap or force a decision. Each probe has a consistent micro-structure:

- **Name** — a short label for the move (e.g. "Challenge against the glossary").
- **Trigger condition** — when to fire it ("When the user uses a term that conflicts with...").
- **Example phrasing** — a concrete sample question, in quotes, showing tone and specificity.
- **Resulting action** — what happens once the probe lands (usually: capture the resolved
  decision into a doc immediately, not batched).

Probes are the reusable "how" — they can be invoked opportunistically whenever their trigger
condition arises during the conversation, not just when their line of inquiry is "active."

## 3. Coverage checklist

A **single, live checklist** enumerating every probe across every line of inquiry, kept
visible/updated throughout the session. Its job:

- Acts as the **exit gate** — the interview cannot be declared done until every item is
  checked or explicitly marked not-applicable *with a reason*.
- Prevents the "ran two lines of inquiry, forgot the third" failure mode.
- Is a flat checklist grouped by line-of-inquiry heading, one line per probe — not
  per-question, per-probe.

## Reusable template for future "grilling"-style skills

```markdown
## Lines of inquiry

The interview must cover **all N lines of inquiry**: [Line A], [Line B], [Line C]. Do not skip
a line of inquiry, and do not skip any probe within one. These are not a batch to run
top-to-bottom: they are the branches the interview walks, one question at a time.

### Coverage checklist

Keep this checklist alive throughout the session. Tick each probe off only once genuinely
covered, and do not conclude until every probe is checked (or explicitly ruled
not-applicable, with a reason).

```
<skill-name> coverage:
[Line A]
- [ ] <Probe 1 name>
- [ ] <Probe 2 name>
- [ ] Update <artifact> inline
[Line B]
- [ ] <Probe 1 name>
- [ ] ...
```

### Line of inquiry: [Line A] (→ <artifact>)

**Probe — <Probe name>**

<When to fire it>. "<Example question in the agent's voice.>"

**Probe — Update <artifact> inline**

When a point is resolved, capture it in <artifact> right there — don't batch, capture each
as it happens.
```

## Invariants to preserve when reusing this template

- Every probe must have: a trigger condition, an example question, and (if it feeds a doc) an
  inline-capture step.
- The checklist mirrors the probes exactly — no probe without a checklist line, no checklist
  line without a probe.
- "Not applicable" is a valid checklist resolution, but it requires a stated reason — silent
  skipping isn't allowed.
</content>
</invoke>
