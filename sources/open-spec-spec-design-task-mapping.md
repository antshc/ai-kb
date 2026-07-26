# Spec → Design → Task: Mapping Guide

## The Principle

> *"Reference specs for what needs to be built, design for how to build it."*

**Specs answer "what done looks like."**  
**Design answers "where and how to implement it."**  
A well-formed task fuses both — so an implementer never needs to look elsewhere.

---

## The Mapping Structure

| Source | Contribution to a Task |
|---|---|
| **Spec** — requirement title | Task's *goal* (what capability is being built) |
| **Spec** — acceptance criterion | Task's *done condition* (the observable behavior that proves it works) |
| **Design** — decision | Task's *implementation target* (exact class, method, or file to change) |
| **Design** — non-goals | Task's *scope boundary* (what to explicitly exclude) |

---

## Worked Example: Loyalty Discount

The following traces a single requirement all the way to tasks, using the e-commerce loyalty discount feature.

### Step 1 — The Requirement (spec.md)

> **Order total must apply a loyalty discount before checkout.**
>
> When a registered user with an active loyalty membership proceeds to checkout, the system must reduce the order total by the discount rate tied to their membership tier.
>
> **Acceptance Criteria**
> - Apply a **tier-based discount** (Bronze: 5%, Silver: 10%, Gold: 15%) to the order subtotal before tax calculation.
> - **Do not apply a discount** if the user has no active loyalty membership.
> - **Do not apply a discount** to items marked as **non-discountable**.
> - Display the **discount amount as a separate line item** in the order summary.

The requirement names four behaviors. Each one will become a subtask.

---

### Step 2 — The Design Decision (design.md)

> **Introduce `LoyaltyDiscountCalculator` called from `OrderPricingService`**
>
> `OrderPricingService.CalculateTotals()` will call **`ILoyaltyDiscountCalculator.Calculate(cart, membershipTier)`** before passing the result to the tax engine. The implementation **`LoyaltyDiscountCalculator`** iterates only over cart items where `Item.IsDiscountable == true`, multiplies each eligible item's subtotal by the tier rate from a **static `TierRateMap` dictionary**, and returns a `DiscountResult` containing the amount and a line-item label. When `membershipTier` is `null` (no active membership), the calculator returns a **zero-value `DiscountResult`** without iterating the cart.

The design names the types, the call sequence, and the null-path behavior. These go directly into the tasks.

---

### Step 3 — The Tasks (tasks.md)

```
## 4. Loyalty Discount

- [ ] 4.1  Add ILoyaltyDiscountCalculator interface with
           Calculate(IReadOnlyList<CartItem> items, MembershipTier? tier): DiscountResult
           to the Pricing.Contracts project.

- [ ] 4.2  Implement LoyaltyDiscountCalculator: filter to item.IsDiscountable == true,
           apply rate from TierRateMap (Bronze=0.05, Silver=0.10, Gold=0.15);
           return DiscountResult.Zero when tier is null.

- [ ] 4.3  Update OrderPricingService.CalculateTotals() to call
           ILoyaltyDiscountCalculator.Calculate() *before* invoking the tax engine;
           pass returned DiscountResult to the order summary builder as a separate line item.

- [ ] 4.4  Add unit tests: no discount when tier is null; correct amount per tier;
           non-discountable items excluded; discount line item present in order summary output.
```

---

### Step 4 — The Connection Map

```
Requirement AC                              →  Design Decision                     →  Task
────────────────────────────────────────────────────────────────────────────────────────────────
"tier-based discount Bronze/Silver/Gold"    →  "TierRateMap dictionary"             →  4.2: TierRateMap with three rate constants
                                                                                        4.4: test correct amount per tier

"not apply if no active membership"         →  "return DiscountResult.Zero          →  4.2: return DiscountResult.Zero when tier is null
                                                when tier is null"                      4.4: test null tier case

"not apply to non-discountable items"       →  "filter to IsDiscountable == true"   →  4.2: filter IsDiscountable == true
                                                                                        4.4: test non-discountable excluded

"discount as a separate line item"          →  "pass DiscountResult to order        →  4.3: pass to order summary builder
                                                summary builder"                        as a separate line item
```

---

## The "AC + Decision" Formula

Apply this formula when writing each subtask:

```
[Verb] [Class/Method from Design] so that [Behavior from AC]; [constraint from negative/edge AC]
```

### Before (spec only — imprecise):
> - [ ] Apply a loyalty discount at checkout.

### After (spec + design fused — precise):
> - [ ] Implement `LoyaltyDiscountCalculator`: filter to `item.IsDiscountable == true`, apply rate from `TierRateMap` (`Bronze=0.05`, `Silver=0.10`, `Gold=0.15`); return `DiscountResult.Zero` when `tier` is `null`.

The fused form tells the implementer the **class to create**, the **filter logic**, the **exact rate values**, and the **null-path behavior** — all without opening another document.

---

## Why Each Design Term Matters in the Task

| Term in task | Origin | Why it must appear |
|---|---|---|
| `TierRateMap` | Design, not spec | Without this name, the implementer might use a switch/if or store rates in config — both conflict with the design. |
| `DiscountResult.Zero` | Design, not spec | The spec only says "do not apply". The task must encode *how* — a sentinel value, not a null check or bool flag. |
| `IsDiscountable == true` | Design operationalizing the AC | The spec says "non-discountable items". The design resolves it to a property; the task names it so there is no ambiguity. |
| `before invoking the tax engine` | Both spec and design | The ordering constraint is implied by the spec, made explicit in design. Missing it from the task risks a silent correctness bug. |
| `ILoyaltyDiscountCalculator` | Design only | Not in the spec at all. Without it in the task, an implementer may embed the logic directly in `OrderPricingService`, breaking testability. |

---

## Key Mapping Points

1. **Requirement → Task group**: Each spec requirement (`###` heading) maps to one task group (`## N.`). One requirement = one coherent area of the codebase.

2. **Acceptance criterion → Subtask**: Each AC contains one observable behavior. One AC = one subtask. The criterion is the implicit verification step.

3. **Design decision → Implementation anchor**: Each design decision names specific types, methods, or files. Copy them into the task so the implementer never guesses the intended structure.

4. **Negative/edge criteria → Explicit constraints**: "must not" and "when absent" criteria are the most commonly dropped. Name them explicitly in the task, including the exact return value or behavior.

5. **Delta verb → Task verb**: Use "Add", "Update", or "Remove" to signal intent at a glance.

---

## The Core Rule

> **A task is precise when you can implement it without re-reading spec or design.**

That requires three things in every task:
- the **behavior** from the acceptance criterion — what "done" looks like,
- the **symbol names** from the design decision — where and how to implement it,
- the **constraint** from negative and edge-case criteria — what must not happen.
