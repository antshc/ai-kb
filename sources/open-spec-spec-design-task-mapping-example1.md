# Example 2: E-Commerce Loyalty Discount

A self-contained example from the e-commerce domain showing the clear connection between Requirement → Design Decision → Task.

---

## Requirement (spec.md)

> ### Order total must apply a loyalty discount before checkout.
>
> When a registered user with an active loyalty membership proceeds to checkout, the system must reduce the order total by the discount rate tied to their membership tier.
>
> #### Acceptance Criteria
> - The system must apply a **tier-based discount** (Bronze: 5%, Silver: 10%, Gold: 15%) to the order subtotal before tax calculation.
> - The system must **not apply a discount** if the user has no active loyalty membership.
> - The system must **not apply a discount** to items marked as **non-discountable**.
> - The system must display the **discount amount as a separate line item** in the order summary.

---

## Design Decision (design.md)

> ### Introduce `LoyaltyDiscountCalculator` called from `OrderPricingService`
>
> `OrderPricingService.CalculateTotals()` will call **`ILoyaltyDiscountCalculator.Calculate(cart, membershipTier)`** before passing the result to the tax engine. The implementation **`LoyaltyDiscountCalculator`** iterates only over cart items where `Item.IsDiscountable == true`, multiplies each eligible item's subtotal by the tier rate from a **static `TierRateMap` dictionary**, and returns a `DiscountResult` containing the amount and a line-item label. When `membershipTier` is `null` (no active membership), the calculator returns a **zero-value `DiscountResult`** without iterating the cart.

---

## Task (tasks.md)

> ## 4. Loyalty Discount
>
> - [ ] 4.1 Add **`ILoyaltyDiscountCalculator`** interface with `Calculate(IReadOnlyList<CartItem> items, MembershipTier? tier): DiscountResult` to the `Pricing.Contracts` project.
> - [ ] 4.2 Implement **`LoyaltyDiscountCalculator`**: filter to `item.IsDiscountable == true`, apply rate from **`TierRateMap`** (`Bronze=0.05`, `Silver=0.10`, `Gold=0.15`); return **`DiscountResult.Zero`** when `tier` is `null`.
> - [ ] 4.3 Update **`OrderPricingService.CalculateTotals()`** to call `ILoyaltyDiscountCalculator.Calculate()` **before invoking the tax engine**; pass returned `DiscountResult` to the order summary builder as a **separate line item**.
> - [ ] 4.4 Add unit tests: no discount when `tier` is `null`; correct amount per tier; **non-discountable items excluded**; discount line item present in order summary output.

---

## Connection Map

```
Requirement AC                           →  Design Decision                    →  Task
─────────────────────────────────────────────────────────────────────────────────────────────
"tier-based discount                     →  "TierRateMap dictionary             →  Task 4.2: TierRateMap with
 Bronze/Silver/Gold"                         with static rates"                     three rate constants

"not apply discount if no                →  "return DiscountResult.Zero         →  Task 4.2: return DiscountResult.Zero
 active membership"                          when tier is null"                     Task 4.4: test null tier case

"not apply to non-discountable items"    →  "filter to                          →  Task 4.2: filter IsDiscountable == true
                                             item.IsDiscountable == true"           Task 4.4: test non-discountable excluded

"discount as separate line item"         →  "pass DiscountResult to             →  Task 4.3: pass to order summary builder
                                             order summary builder"                  as separate line item
```

---

## Why Each Bold Term Matters

- **`tier-based discount`** — the requirement states *what*, but not the data structure. The design resolves it to **`TierRateMap`** (a dictionary). The task encodes the exact key-value pairs (`Bronze=0.05`) so the implementer never guesses the rates.

- **`not apply a discount`** (negative constraint, appears twice) — two separate conditions: no membership, and non-discountable items. The design folds both into one path (return zero early; filter before iterating). Tasks 4.2 and 4.4 each enforce one of these conditions explicitly, so neither gets forgotten during implementation.

- **`ILoyaltyDiscountCalculator`** — not in the requirement at all. It comes purely from the design decision (testability, single responsibility). Without copying this name into the task, an implementer might embed the logic directly inside `OrderPricingService`, making it untestable and violating the design.

- **`DiscountResult.Zero`** — a design-originated sentinel value. The requirement only says "do not apply". The design decides *how* — a zero value object rather than a null check or a `bool` flag. The task preserves this name so the implementer builds the right type.

- **`before invoking the tax engine`** — the ordering constraint. The requirement implies it (discount before tax), the design makes it explicit, and task 4.3 locks it in as a sequencing requirement on the call in `CalculateTotals()`. If this phrase were missing from the task, the implementer might apply the discount after tax — a silent correctness bug.

---

## The Pattern in One Line

> The **requirement names the behavior**, the **design names the types and sequence**, the **task combines both** so implementation needs no additional lookup.
