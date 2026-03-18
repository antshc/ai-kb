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
