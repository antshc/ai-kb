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
- State the required outcome, not hidden reasoning.

## 5. Variable Standard

Variables declared inside agent or skill instructions are conventions interpreted by the agent. They are not automatically created environment variables.

### Syntax

| Syntax | Meaning | Example |
|---|---|---|
| `` `camelCase` `` | Conceptual value resolved and maintained by the agent | Resolve `repositoryRoot` from Git. |
| `UPPER_SNAKE_CASE := instruction` | Runtime assignment evaluated by the agent | `NAME := generate a unique kebab-case name` |
| `<UPPER_SNAKE_CASE>` | Placeholder replaced with a resolved runtime value | `reports/<NAME>.md` |
| `<!-- ... -->` | Hidden template instruction not rendered in Markdown preview | `<!-- Remove this comment after population. -->` |
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

### Hidden Instructions

Use HTML comments for instructions that MUST remain invisible in Markdown preview:

```markdown
<!--
NAME := generate a unique lowercase kebab-case name
Remove this comment from the populated output.
-->

# Project: <NAME>
```

HTML comments MUST NOT be nested. The template MUST state whether comments remain in source or are removed from generated output.

### Variable Rules

- Define each value before first use.
- State its source, fallback, and validation.
- Resolve assignments in declaration order.
- Replace all placeholders before producing output.
- Pass conceptual values explicitly to commands or subagents.
- Use `$VARIABLE` only for real shell environment variables.
- Use `${{ ... }}` only in supported GitHub expression contexts.
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

Define runtime values, then populate the object:

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

| Form | Injected JSON type |
|---|---|
| `"<NAME>"` | String |
| `<COUNT>` | Number |
| `<ENABLED>` | Boolean |
| `<ITEMS>` | Array |
| `<CONFIG>` | Object |
| `null` | Null |

Quoted placeholders inject strings. Unquoted placeholders inject complete JSON values.

### Array Mapping

Apply instructions once per input object:

```markdown
RESULTS := SOURCE_ITEMS map ITEM => {
  "id": generate UUID,
  "name": kebab-case ITEM.name,
  "source": ITEM.path,
  "enabled": ITEM.active
}
```

Use `INDEX` when position is required:

```markdown
RESULTS := SOURCE_ITEMS map (ITEM, INDEX) => {
  "order": INDEX + 1,
  "name": kebab-case ITEM.name
}
```

Rules:

- `SOURCE_ITEMS` MUST be an array.
- `ITEM` represents the current object.
- `INDEX` represents the zero-based position.
- Input order MUST be preserved unless otherwise specified.
- Final output MUST be valid JSON with no unresolved placeholders.

## 7. Template Conventions

| Convention | Standard |
|---|---|
| Strictness | Declare `EXACT` or `DEFAULT` |
| Placeholder | Use `<UPPER_SNAKE_CASE>` |
| Runtime assignment | Use `NAME := instruction` |
| Hidden instruction | Use `<!-- ... -->` |
| Optional section | Mark explicitly as `OPTIONAL` |
| Repeated section | Use `SOURCE map ITEM => ...` |
| Conditional section | Use `IF condition THEN ...` |
| Missing values | Define `omit`, `null`, or a default |
| Ordering | Define deterministic field or section order |
| Validation | Require valid format and zero unresolved placeholders |

### Strictness

```markdown
TEMPLATE_MODE := EXACT
```

`EXACT` MUST preserve headings, order, field names, and required sections.

```markdown
TEMPLATE_MODE := DEFAULT
```

`DEFAULT` MAY adapt or omit sections when irrelevant.

### Required, Optional, and Conditional Content

```markdown
<!-- REQUIRED -->
## Summary
<SUMMARY>

<!-- OPTIONAL: omit when WARNINGS is empty -->
## Warnings
<WARNINGS>
```

```markdown
IF WARNINGS is not empty:
  include `## Warnings`
ELSE:
  omit the section
```

### Replaceable Regions

```markdown
<!-- BEGIN GENERATED:FINDINGS -->
<FINDING_BLOCKS>
<!-- END GENERATED:FINDINGS -->
```

Only content between matching markers MUST be replaced. Content outside the region MUST be preserved.

### Missing Values

Define one policy per value:

```markdown
OWNER := user value; otherwise null
DESCRIPTION := user value; otherwise omit field
STATUS := user value; otherwise "pending"
```

Empty strings SHOULD NOT represent missing values unless required by the target schema.

### Escaping

- JSON strings MUST use JSON escaping.
- Markdown table pipes MUST be escaped as `\|`.
- YAML strings containing `:`, `#`, or leading special characters SHOULD be quoted.
- Nested code fences MUST use a longer outer fence or an alternative fence marker.

### Validation

Before writing the result:

1. Replace all placeholders.
2. Remove template-only comments when required.
3. Verify required sections exist.
4. Remove empty optional sections.
5. Validate the target format or schema.
6. Preserve declared ordering.

Long templates SHOULD have one source of truth under `assets/` or `references/`; instructions MUST reference the file instead of recreating it from memory.

## 8. Workflow Standard

Each significant workflow step SHOULD define:

```markdown
### Step 2 — Validate Changes

**Input:** `changedFiles`  
**Action:** Run project tests and static analysis.  
**Output:** `validationResult`  
**Success:** All required checks pass.  
**Failure:** Record the command, exit code, and relevant error.
```

- Steps MUST be ordered.
- Each step MUST have a measurable completion condition.
- Dependencies MUST be explicit.
- Editing workflows MUST end with validation.
- Findings MUST include evidence such as `path/to/file.cs:42`.
- Agents MUST NOT claim success without running declared checks.
- Destructive actions MUST require explicit user intent.

## 9. Output Contract

Every agent MUST define an exact output contract.

- Output MUST lead with the primary result or status.
- Only executed commands and produced artifacts MUST be reported.
- `failed`, `blocked`, and `not-run` MUST remain distinct.
- Empty results MUST be explicit, such as `[]`, `No changes`, or `No findings`.
- Section and field ordering SHOULD be deterministic.
- Hidden reasoning MUST NOT be exposed.

### Machine-Readable Output

Use JSON when another agent or automation consumes the result. The contract MUST define field names, types, enums, ordering, empty-result behavior, and whether additional prose is allowed.

Compact field-level contract:

```json
[
  {
    "AXIS": "code-smells",
    "FILE_PATH": "<repo-relative changed-file path>",
    "LINE_NUMBER": <positive integer; new RIGHT-side diff line; last line of a range>,
    "LABEL": "<actionable smell: suggest | minor smell: nit | no smell: omit object | MUST NOT be bug or blocking>",
    "REVIEW_COMMENT": "<LABEL>: <issue → impact → fix; MUST omit the smell name; format via /to-review-comment>"
  }
]
```

- Each object MUST represent one issue.
- The array MUST contain at most five objects.
- Output MUST contain JSON only, with no Markdown fences, prose, or unresolved placeholders.
- Results SHOULD order `suggest` before `nit`, then by file and line.
- The agent MUST return `[]` when no actionable, net-new smell is found.

General JSON rules:

- A fixed schema MUST be used.
- Field types MUST remain stable.
- Status fields SHOULD use enums.
- JSON MUST be valid and contain no comments.
- Optional fields MAY be omitted only when the contract permits it.

## 10. Resources

Follow:

- [Agent Skills specification](https://agentskills.io/specification)
- [Awesome Copilot skill guidelines](https://github.com/github/awesome-copilot/blob/main/instructions/agent-skills.instructions.md)

## 11. Plugin Manifest

Follow:

- [GitHub Copilot plugin documentation](https://docs.github.com/en/copilot/customizing-copilot/extending-copilot-chat-with-mcp)
- [Awesome Copilot repository guidelines](https://github.com/github/awesome-copilot/blob/main/AGENTS.md)

## 12. Quality Gate

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
