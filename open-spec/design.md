## What Is Context in a Design Document

Context is the **"why now" and "what exists"** section. It gives a reader everything they need to understand the design decisions without having to read the codebase first.

It answers three questions:

| Question | What to write |
|---|---|
| **What is the current state?** | How the system works today, before this change |
| **What is the problem?** | Why the current state is insufficient |
| **What already exists that we will build on?** | Code, patterns, or constraints the design must work within |

---

## How It Is Used

**By the design author** — written first, before decisions. Forces you to articulate the problem clearly before proposing solutions. If you can't write the context, the problem isn't understood yet.

**By reviewers** — lets them evaluate decisions without needing codebase knowledge. They can immediately see whether a decision fits the constraints.

**By implementers** — tells them which existing code to touch and which to leave alone, before they open any files.

**By future readers** — six months later, when someone asks "why was this done?", the context is the answer.

---

## The Three Parts of Context
**Current state:** How the system works today.
Be specific — name the class, method, or config that owns the behavior.

**Problem:** Why the current state is insufficient.
One or two sentences. If you need more, the problem isn't clear yet.

**Existing code** What you will build on — and what you will NOT touch.
to build on: "X already does Y — no structural changes required there"
is just as important as "we will add Z".



---

## The Failure Mode Without Context

Without it, a reviewer seeing a decision has no idea:
- why the current approach was insufficient,
- whether existing components need changes,
- what backward compatibility constraints exist.

They either approve blindly or ask questions that the context section would have answered upfront.

---

## The Test

> *"Can a reviewer evaluate my decisions without opening a single source file?"*  
> If yes — context is sufficient. If no — something is missing.


## Goals / Non-Goals

**Goals** declare what this design commits to delivering — each one maps to code you will write.  
**Non-Goals** declare what this design refuses to solve — each one preempts a question someone will ask during review.

Neither is a summary of requirements. They are a **scope contract between authors and implementers**.

---

## Example: Payment Processing Design

**Goals:**
- Charge the customer's stored payment method when an order is submitted.
- Retry a failed charge up to 3 times with exponential backoff.
- Emit a `PaymentSucceeded` / `PaymentFailed` event after the final attempt.

**Non-Goals:**
- Adding new payment providers (Stripe is the only provider in scope).
- Refund processing — handled by a separate refund flow.
- Fraud detection — the payment gateway handles it; we do not inspect charge results for fraud signals.

---

## Why Non-Goals Matter More Than Goals

The goals are usually obvious from the spec. The non-goals are not — they answer the questions an implementer would *silently assume* are included:

> *"While I'm touching the charge logic, should I also handle refunds?"*  
> → Non-goal: **no**. Separate flow. Don't touch it.

> *"Should I validate the fraud score before retrying?"*  
> → Non-goal: **no**. Gateway handles it. Don't add that code.

Without non-goals, scope expands silently during implementation. With them, the boundary is explicit before a single line is written.

---

## The Test

- **Goal**: *"Will I write code specifically for this?"* → Yes → it's a goal.
- **Non-goal**: *"Would a reasonable engineer assume this is included?"* → Yes → it must be a non-goal.
