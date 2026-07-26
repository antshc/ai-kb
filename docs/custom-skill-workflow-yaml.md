# Custom Skill `workflow.yaml`

## Summary

`workflow.yaml` is **not** a standard executable file for GitHub Copilot or Claude Agent Skills.

The standard skill entry point is `SKILL.md` with YAML frontmatter. A skill may include scripts, references, templates, and data files that `SKILL.md` explicitly tells the agent how to use.

Use `workflow.yaml` only as a custom, machine-readable workflow contract when:

- the workflow has multiple phases;
- dependencies and gates must be explicit;
- an agent, script, or orchestrator validates and interprets the file;
- the same workflow definition must be reused across agents or tools.

Without an interpreter or explicit `SKILL.md` instructions, `workflow.yaml` is only reference data.

## Recommended Structure

```text
.github/skills/feature-workflow/
├── SKILL.md
├── workflow.yaml
├── schemas/
│   └── workflow.schema.json
├── scripts/
│   ├── validate-workflow.py
│   └── run-gate.sh
└── references/
    └── phase-guidance.md
```

`SKILL.md` remains the controller. `workflow.yaml` provides structured workflow data. Scripts perform deterministic validation and execution.

## Responsibility Split

| Artifact | Responsibility |
|---|---|
| `SKILL.md` | Activation, reasoning instructions, execution rules, failure handling, and output contract |
| `workflow.yaml` | Phases, dependencies, artifacts, gates, retries, and policy values |
| `workflow.schema.json` | Structural validation and allowed values |
| `scripts/` | Deterministic checks, transformations, and command execution |
| Runtime state | Current phase, attempts, outcomes, evidence, and resume point |

Do not store mutable execution state in `workflow.yaml`. Keep it as the workflow definition and persist runtime state separately.

## Example `workflow.yaml`

```yaml
schema-version: 1
workflow: feature-delivery

phases:
  - id: discover
    output: .workflow/requirements.md
    success:
      command: scripts/validate-requirements.sh
    failure: retry

  - id: design
    depends-on: [discover]
    input: .workflow/requirements.md
    output: .workflow/design.md
    success:
      command: scripts/validate-design.sh
    failure: return-to-discover

  - id: implement
    depends-on: [design]
    input: .workflow/design.md
    success:
      command: dotnet build
    failure: fix-and-retry

  - id: verify
    depends-on: [implement]
    success:
      commands:
        - dotnet test
        - dotnet format --verify-no-changes
    failure: fix-and-retry
```

The schema is project-defined. GitHub Copilot and Claude do not assign built-in meaning to these fields.

## Required `SKILL.md` Instructions

```markdown
## Workflow

1. Read `workflow.yaml` from this skill directory.
2. Validate it against `schemas/workflow.schema.json`.
3. Execute phases in dependency order.
4. Do not start a phase until all dependencies have succeeded.
5. Produce every declared output artifact.
6. Run every declared success gate.
7. Apply the declared failure policy when a gate fails.
8. Persist phase status and the exact resume point after each phase.
9. Never silently skip an unknown field, phase, dependency, or failure policy.
10. Complete only when every required phase has a terminal outcome.
```

The skill must define how paths are resolved, which fields are required, which commands require approval, and what happens when validation fails.

## Execution Model

```text
load SKILL.md
    ↓
load workflow.yaml
    ↓
validate schema
    ↓
resolve dependencies
    ↓
execute phase
    ↓
validate gate
    ↓
persist outcome
    ↓
continue, retry, return, or stop
```

Treat each phase as a contract:

```text
inputs
preconditions
actions
outputs
success gate
failure policy
```

## Validation Rules

A workflow interpreter SHOULD verify:

- the schema version is supported;
- phase IDs are unique;
- dependencies reference existing phases;
- the dependency graph is acyclic;
- referenced scripts and paths exist;
- every phase has a measurable completion gate;
- failure-policy values are known;
- destructive commands require explicit user intent;
- completed phases have observable evidence;
- no required phase remains `not-started` or `in-progress` at completion.

For high-risk workflows, generate an execution plan from `workflow.yaml`, validate it, and only then execute commands.

## What Belongs in YAML

Use YAML for structured, stable values:

- phase identifiers;
- dependencies;
- inputs and outputs;
- commands and script paths;
- retry limits;
- timeouts;
- allowed outcome values;
- validation gates;
- artifact paths.

Keep these in Markdown instead:

- judgment rules;
- domain guidance;
- nuanced trade-offs;
- examples requiring explanation;
- escalation guidance;
- user-facing output requirements.

Avoid encoding long natural-language prompts inside YAML. YAML is most useful when fields can be validated and interpreted consistently.

## Distinguish Similar Formats

| Format | Meaning |
|---|---|
| Skill `SKILL.md` frontmatter | Standard skill metadata such as `name`, `description`, and optional tool settings |
| Custom skill `workflow.yaml` | Project-defined supporting resource with no built-in execution semantics |
| `.github/workflows/*.yml` | GitHub Actions workflow executed by the Actions runner |
| GitHub agentic workflow `.md` | YAML frontmatter plus natural-language agent instructions |
| GitHub agentic workflow `.lock.yml` | Compiled hardened Actions workflow; do not edit manually |

Do not place a custom skill workflow in `.github/workflows/` unless it is a valid GitHub Actions workflow.

## When Not to Use `workflow.yaml`

Keep the workflow entirely in `SKILL.md` when:

- it is short and linear;
- phases are not reused;
- no machine validation is required;
- the YAML would duplicate the Markdown instructions;
- no script or orchestrator consumes the structured definition.

Use separate specialized skills when phases have independent activation triggers, permissions, or reusable expertise. Use subagents when work can be delegated through explicit input and output artifacts.

## Recommended Rule

> Markdown defines how the agent should reason and behave. YAML defines structured workflow data. Scripts provide deterministic guarantees.

## References

- [GitHub: Adding agent skills for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [GitHub: Copilot CLI skill reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#skills-reference)
- [GitHub: About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [GitHub: About agentic workflows](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/about-github-agentic-workflows)
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Agent Skills specification](https://agentskills.io/specification)
