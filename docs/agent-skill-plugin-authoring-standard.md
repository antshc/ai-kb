# Agent, Skill, and Plugin Authoring Standard

Use RFC 2119 terms: **MUST**, **MUST NOT**, **SHOULD**, **MAY**.

## 1. File Naming

Follow:

- [Custom agent guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agents.instructions.md)
- [Agent skill guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agent-skills.instructions.md)
- [Repository and plugin contribution guidelines](https://github.com/github/awesome-copilot/blob/main/AGENTS.md)

## 2. Agent Frontmatter

Follow:

- [GitHub custom agent frontmatter reference](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Awesome Copilot agent guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agents.instructions.md)

## 3. Skill Frontmatter

Follow:

- [GitHub agent skill format](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [Awesome Copilot skill guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agent-skills.instructions.md)

## 4. Instruction Structure

Use this order when applicable:

```markdown
# <Agent or Skill Name>

## Role
One sentence defining responsibility.

## Inputs
Required, optional, and derived values.

## Preconditions
Required tools, files, environment, or repository state.

## Workflow
Ordered executable steps.

## Constraints
Scope limits, invariants, and prohibited actions.

## Validation
Commands and checks proving completion.

## Output Contract
Exact response or artifact schema.

## Failure Handling
Expected behavior for blockers and partial failures.

## Gotchas
Non-obvious constraints or known failure modes.

## References
Relative links to supporting resources.
```

Instructions MUST:

- Use imperative mood: `Read`, `Search`, `Run`, `Create`.
- Define observable actions.
- Avoid vague verbs such as `handle`, `consider`, or `improve`.
- Separate workflow, constraints, validation, and output.
- Avoid repeating general knowledge already known by the model.
- State the required outcome, not hidden reasoning.

## 5. Variable Standard

Variables declared inside agent or skill instructions are conventions interpreted by the agent. They are not automatically created environment variables.

### Syntax

| Syntax | Meaning | Example |
|---|---|---|
| `` `camelCase` `` | Conceptual value resolved and maintained by the agent | Resolve `repositoryRoot` from Git. |
| `UPPER_SNAKE_CASE := instruction` | Runtime assignment evaluated by the agent | `NAME := generate a unique kebab-case name` |
| `<UPPER_SNAKE_CASE>` | Placeholder replaced with a resolved runtime value | `reports/<NAME>.md` |
| `[optional]` | Optional input or argument | `[target-path]` |
| `value1 \| value2` | Allowed values | `completed \| failed \| blocked` |
| `` `literal` `` | Fixed command, path, identifier, or value | Run `dotnet test`. |
| `$VARIABLE` | Shell environment variable | `cd "$REPOSITORY_ROOT"` |
| `${VARIABLE}` | Braced shell environment variable | `${REPOSITORY_ROOT}/src` |
| `export VARIABLE=value` | Assign a shell variable for the current shell | `export CONFIGURATION=Release` |
| `VARIABLE=value command` | Assign a variable for one command | `CONFIGURATION=Release dotnet build` |
| `${{ vars.NAME }}` | GitHub Actions configuration variable | `${{ vars.DEPLOY_REGION }}` |
| `${{ secrets.NAME }}` | GitHub Actions secret | `${{ secrets.API_TOKEN }}` |
| `${{ inputs.NAME }}` | GitHub Actions input | `${{ inputs.target-path }}` |
| `${{ env.NAME }}` | GitHub Actions environment variable | `${{ env.CONFIGURATION }}` |

### Runtime Assignment

Use `:=` when the right side is an instruction evaluated during execution:

```markdown
NAME := generate a unique lowercase kebab-case name
TIMESTAMP := current UTC timestamp in ISO 8601 format
OUTPUT_PATH := reports/<NAME>.md
```

Evaluation order:

1. Execute the instruction on the right.
2. Store the result under the name on the left.
3. Replace matching placeholders before producing output.

Example:

```markdown
NAME := generate a unique lowercase kebab-case name
OUTPUT_PATH := reports/<NAME>.md

Create `<OUTPUT_PATH>`.
```

Resolved values:

```text
NAME = silent-river
OUTPUT_PATH = reports/silent-river.md
```

Resolved instruction:

```markdown
Create `reports/silent-river.md`.
```

### Instruction Context Example

```markdown
## Inputs

| Name | Type | Required | Default | Source | Validation |
|---|---|---:|---|---|---|
| `repositoryRoot` | path | Yes | — | Git | Directory exists |
| `targetPath` | path | No | `repositoryRoot` | User input | Path exists inside repository |
| `configuration` | enum | No | `Release` | User input | `Debug` or `Release` |
| `reportPath` | path | No | `repositoryRoot/reports/review.md` | Derived | Parent is writable |

## Workflow

1. Run `git rev-parse --show-toplevel`.
2. Set `repositoryRoot` to the command output.
3. Set `targetPath` to the user-provided path; otherwise use `repositoryRoot`.
4. Set `configuration` to the user-provided value; otherwise use `Release`.
5. Set `reportPath` to `repositoryRoot/reports/review.md`.
6. Validate all resolved values.
7. Pass values explicitly to the script:

   ```bash
   TARGET_PATH="<resolved-target-path>" \
   CONFIGURATION="<resolved-configuration>" \
   ./scripts/validate.sh
   ```
```

### Variable Rules

- Define each value before first use.
- Use descriptive names.
- State the value source.
- Define fallback behavior.
- Validate resolved values.
- Resolve assignments in declaration order.
- Replace all placeholders before producing output.
- Pass conceptual values explicitly to commands or subagents.
- Use `$VARIABLE` only for real shell environment variables.
- Use `${{ ... }}` only in supported GitHub expression contexts.
- Do not use `${camelCase}` for conceptual values.
- Do not assume automatic interpolation.

Avoid:

```markdown
NAME: { random name }
```

Prefer:

```markdown
NAME := generate a random name
```

## 6. JSON Population

### Object Population

Define runtime values, then populate the JSON object:

```markdown
NAME := generate a unique kebab-case name
ID := generate a UUID
ENABLED := true
TAGS := ["copilot", "skill"]

Populate:

{
  "id": "<ID>",
  "name": "<NAME>",
  "enabled": <ENABLED>,
  "tags": <TAGS>
}
```

Placeholder types:

| Form | Injected JSON type |
|---|---|
| `"<NAME>"` | String |
| `<COUNT>` | Number |
| `<ENABLED>` | Boolean |
| `<ITEMS>` | Array |
| `<CONFIG>` | Object |
| `null` | Null |

Quoted placeholders inject strings.

Unquoted placeholders inject complete JSON values.

### Array Mapping

Apply instructions to every input object:

```markdown
RESULTS := SOURCE_ITEMS map ITEM => {
  "id": generate UUID,
  "name": kebab-case ITEM.name,
  "source": ITEM.path,
  "enabled": ITEM.active
}
```

Use `INDEX` when the position is required:

```markdown
RESULTS := SOURCE_ITEMS map (ITEM, INDEX) => {
  "order": INDEX + 1,
  "name": kebab-case ITEM.name
}
```

Example input:

```json
[
  {
    "name": "Payment Service",
    "path": "src/payments",
    "active": true
  },
  {
    "name": "Order Service",
    "path": "src/orders",
    "active": false
  }
]
```

Expected result:

```json
[
  {
    "id": "generated-uuid-1",
    "name": "payment-service",
    "source": "src/payments",
    "enabled": true
  },
  {
    "id": "generated-uuid-2",
    "name": "order-service",
    "source": "src/orders",
    "enabled": false
  }
]
```

Rules:

- `SOURCE_ITEMS` MUST be an array.
- `ITEM` represents the current object.
- `INDEX` represents the zero-based position.
- Mapping instructions execute once per item.
- Input order MUST be preserved unless otherwise specified.
- Source objects MUST NOT be mutated unless explicitly required.
- String placeholders MUST be quoted.
- Array, object, number, and Boolean placeholders MUST remain unquoted.
- Final output MUST be valid JSON.
- No unresolved placeholders may remain.

## 7. Workflow Standard

Each significant workflow step SHOULD define:

```markdown
### Step 2 — Validate Changes

**Input:** `changedFiles`  
**Action:** Run project tests and static analysis.  
**Output:** `validationResult`  
**Success:** All required checks pass.  
**Failure:** Record the command, exit code, and relevant error.
```

Rules:

- Steps MUST be ordered.
- Each step MUST have a measurable completion condition.
- Dependencies MUST be explicit.
- Independent operations SHOULD run in parallel.
- Editing workflows MUST end with validation.
- Findings MUST include evidence such as `path/to/file.cs:42`.
- Agents MUST NOT claim success without running declared checks.
- Destructive actions MUST require explicit user intent.
- Partial completion MUST be reported accurately.

## 8. Output Contract

Every agent MUST define an exact output contract.

Rules:

- Do not include greetings, task restatements, or sign-offs.
- Lead with status or the primary result.
- List changed files and generated artifacts.
- Report only commands actually executed.
- Distinguish `failed`, `blocked`, and `not-run`.
- State `No changes` or `No findings` explicitly.
- Keep section ordering deterministic.
- Omit empty optional sections.
- Never expose hidden reasoning.
- Define field names, types, enums, and ordering.
- Define whether additional prose is allowed.

### Machine-Readable Output

Use JSON when another agent or automation consumes the result:

```json
{
  "status": "completed",
  "summary": "Removed unused code without changing public behavior.",
  "filesChanged": [
    "src/service.ts"
  ],
  "validation": [
    {
      "command": "npm test",
      "status": "passed"
    }
  ],
  "artifacts": [],
  "warnings": [],
  "nextAction": null
}
```

JSON rules:

- Use a fixed schema.
- Use enums for status fields.
- Keep field types stable.
- Omit optional fields only when permitted by the contract.
- Do not wrap JSON in explanatory prose.
- Define maximum array sizes when token control matters.
- Return valid JSON without comments.
- Do not include unresolved placeholders.

## 9. Resources

Follow:

- [Agent Skills specification](https://agentskills.io/specification)
- [Awesome Copilot skill guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agent-skills.instructions.md)

## 10. Plugin Manifest

Follow:

- [GitHub Copilot plugin documentation](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp)
- [Awesome Copilot repository guidelines](https://github.com/github/awesome-copilot/blob/main/AGENTS.md)

## 11. Quality Gate

Verify:

- Frontmatter parses.
- Names and paths match.
- Descriptions include capability and activation triggers.
- Instructions use imperative and observable language.
- Inputs and defaults are documented.
- Runtime assignments are defined before use.
- Placeholder syntax is consistent.
- No unresolved placeholders remain.
- Workflow steps define success and failure conditions.
- Permissions follow least privilege.
- Output is exact and testable.
- JSON output is schema-valid.
- Validation commands exist.
- References use relative paths.
- No secrets or machine-specific absolute paths exist.
- Examples produce the documented output.
