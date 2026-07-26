# Example 1: Password Security

A self-contained example showing the clear connection between Requirement → Design Decision → Task.

---

## Requirement (spec.md)

> ### User password must be stored securely
>
> When a user registers, the system must store their password in a way that prevents recovery even if the database is compromised.
>
> #### Acceptance Criteria
> - The system must **hash** the password using a **cryptographically strong algorithm** before persisting it.
> - The system must use a **unique per-user salt** to prevent rainbow table attacks.
> - The system must **never store or log the plaintext password** at any point.

---

## Design Decision (design.md)

> ### Use BCrypt for password hashing in `UserRegistrationService`
>
> `UserRegistrationService.RegisterAsync()` will call **`IPasswordHasher.Hash(plaintext)`** before passing the result to `IUserRepository.SaveAsync()`. The implementation **`BCryptPasswordHasher`** wraps the **BCrypt.Net** library, which internally generates a **per-call random salt** and embeds it in the output hash. No salt column is needed in the `users` table — the salt is encoded in the **`password_hash` column** value. Plaintext is **zeroed from memory** after hashing using `SecureString` disposal.

---

## Task (tasks.md)

> ## 3. Password Security
>
> - [ ] 3.1 Add **`IPasswordHasher`** interface with `Hash(string plaintext): string` and `Verify(string plaintext, string hash): bool` to the `Auth.Contracts` project.
> - [ ] 3.2 Implement **`BCryptPasswordHasher`** wrapping `BCrypt.Net-Next`, generating a **per-call embedded salt**; dispose the plaintext string via `SecureString` after hashing.
> - [ ] 3.3 Update **`UserRegistrationService.RegisterAsync()`** to call `IPasswordHasher.Hash()` before `IUserRepository.SaveAsync()`; assert the raw password is **never passed to the repository**.
> - [ ] 3.4 Add unit tests: verify the **stored value is not equal to plaintext**, that two hashes of the same input produce **different outputs** (salt randomness), and that `Verify()` returns `true` for matching plaintext.

---

## Connection Map

```
Requirement AC                        →  Design Decision               →  Task
──────────────────────────────────────────────────────────────────────────────────────
"hash with cryptographically           →  "use BCrypt.Net"             →  Task 3.2: implement BCryptPasswordHasher
 strong algorithm"

"unique per-user salt"                 →  "BCrypt embeds salt          →  Task 3.2: "per-call embedded salt"
                                           in the hash output"             Task 3.4: test two hashes differ

"never store plaintext"                →  "zero memory via             →  Task 3.2: SecureString disposal
                                           SecureString disposal"          Task 3.3: never passed to repository

(implicit: testability)                →  "IPasswordHasher interface"  →  Task 3.1: extract interface
                                                                           Task 3.4: write unit tests
```

---

## Why Each Bold Term Matters

- **`hash`** — the requirement names the operation without prescribing the algorithm. The design resolves the ambiguity ("BCrypt"), and the task implements the resolution. If the task had invented a different algorithm, the chain would be broken.

- **`unique per-user salt`** — a testable property. The task maps it to two things: the implementation detail ("per-call embedded salt") and a specific test case ("two hashes of the same input produce different outputs"). The test case *is* the acceptance criterion re-expressed as code.

- **`never store or log the plaintext`** — a negative constraint. The design answers *how* (SecureString disposal, never pass raw to repository). The task enforces both the implementation and an assertion in tests. Without the design decision, a task author might skip the `SecureString` step entirely.

- **`IPasswordHasher`** — this type name does not appear in the requirement at all. It comes entirely from the design decision (testability via interface). This is the key point: **tasks that omit design-originated names are incomplete** — they leave the implementer to re-derive architectural decisions already made.
