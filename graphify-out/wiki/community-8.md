# Community 8

**8 nodes**

## Nodes
### BCryptPasswordHasher
- **File:** `open-spec-spec-design-task-mapping-example2.md`
- **Type:** concept

### ILoyaltyDiscountCalculator
- **File:** `open-spec-spec-design-task-mapping-example1.md`
- **Type:** concept
- **Links:**
  - semantically_similar_to → IPasswordHasher

### IPasswordHasher
- **File:** `open-spec-spec-design-task-mapping-example2.md`
- **Type:** concept

### Loyalty Discount Design Decision
- **File:** `open-spec-spec-design-task-mapping-example1.md`
- **Type:** concept
- **Links:**
  - references → ILoyaltyDiscountCalculator
  - references → LoyaltyDiscountCalculator
  - references → OrderPricingService.CalculateTotals

### LoyaltyDiscountCalculator
- **File:** `open-spec-spec-design-task-mapping-example1.md`
- **Type:** concept

### OrderPricingService.CalculateTotals
- **File:** `open-spec-spec-design-task-mapping-example1.md`
- **Type:** concept

### Password Security Design Decision
- **File:** `open-spec-spec-design-task-mapping-example2.md`
- **Type:** concept
- **Links:**
  - references → BCryptPasswordHasher
  - references → IPasswordHasher
  - references → UserRegistrationService.RegisterAsync

### UserRegistrationService.RegisterAsync
- **File:** `open-spec-spec-design-task-mapping-example2.md`
- **Type:** concept
