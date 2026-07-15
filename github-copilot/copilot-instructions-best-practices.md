# GitHub Copilot Repository Instructions

Best practices and an annotated `.github/copilot-instructions.md` template.

## Purpose

Use repository instructions for rules relevant to most repository tasks:

- Repository topology and boundaries.
- Mandatory safety guards.
- Authoritative documentation.
- Build, test, and validation commands.
- Repository-wide conventions.
- Default tool-selection policies.

Use path-specific instructions or skills for specialized workflows.

## Best practices

### 1. Keep global instructions global

Include only rules that apply to most tasks.

Move conditional detail to:

- `.github/instructions/*.instructions.md` — path-specific rules.
- `.github/skills/<skill>/SKILL.md` — task-specific workflows.
- `AGENTS.md` — directory-scoped agent rules.

Reason: smaller always-loaded context; less noise and fewer conflicts.

### 2. Describe topology before behavior

State:

- What the repository contains.
- Where source, tests, docs, and generated files live.
- Which related repositories or worktrees exist.
- Which paths must not be modified.

Reason: routing rules are unreliable without a clear repository model.

### 3. Use one normative vocabulary

Use consistently:

- `MUST`
- `MUST NOT`
- `SHOULD`
- `MAY`

Avoid mixing `HARD GUARD`, `DO`, `DON'T`, `always`, and `never` as separate severity systems.

### 4. Make rules testable

Good:

> MUST run tests for the changed project before reporting completion.

Weak:

> Ensure the implementation is correct.

A useful rule defines:

- Trigger.
- Required action.
- Target path or repository.
- Verification.
- Stop condition.

### 5. Define exact repository targeting

For multi-repository work, specify:

- Exact `owner/repository` identity.
- Exact working directory.
- Allowed actions per repository.
- Verification command.
- Failure behavior.

Use exact comparisons, not substring checks.

```bash
repo="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
test "$repo" = "<owner/repository>" || exit 1
```

Also verify the filesystem target:

```bash
git rev-parse --show-toplevel
```

### 6. Name authoritative sources

List each source and what it owns:

- Domain terminology.
- Architecture decisions.
- API contracts.
- Coding conventions.
- Build instructions.
- Configuration reference.

When documentation and code disagree, require the agent to report the discrepancy.

### 7. Prefer LSP for semantic navigation

Use LSP for:

- Definitions.
- References.
- Implementations.
- Call hierarchy.
- Type information.
- Symbol-aware rename.

Use `rg`, `grep`, or `find` for:

- String literals.
- Configuration values.
- Generated files.
- Non-code assets.
- LSP fallback.

Do not duplicate the full LSP operation catalog in global instructions. Copilot CLI selects the appropriate LSP operation automatically when available.

### 8. Define LSP fallback precisely

Before falling back to text search:

1. Verify LSP health.
2. Confirm the working directory.
3. Confirm the relevant project or solution is loaded.
4. Reload or reinitialize the server when supported.
5. Build only when project evaluation requires it.

Reason: an empty result does not prove that the symbol does not exist.

### 9. Define validation

Before completion, require the agent to:

1. Inspect the final diff.
2. Run the smallest relevant build.
3. Run tests covering changed behavior.
4. Run required formatting or lint checks.
5. Report checks not run and why.
6. Confirm no files changed in the wrong repository.

Prefer targeted validation over an unnecessary full-solution build.

### 10. Protect secrets explicitly

Require:

- MUST NOT print secret values.
- MUST NOT commit `.env` files.
- MUST NOT copy credentials into issues, docs, logs, or responses.
- Refer to environment variable names, never their values.

### 11. Use progressive disclosure

Keep global instructions short. Put large examples, lookup tables, integration procedures, and scripts in skills or reference files loaded only when needed.

Keep references shallow: link directly from `SKILL.md` to supporting files.

### 12. Remove contradictions and duplication

Each rule should have one authoritative definition.

Common contradictions:

- Docs must be created in one repository, but commits are forbidden there.
- All terminal commands must run in the code repository, but issue and documentation commands run elsewhere.
- The agent must build after any incomplete LSP result, even when the LSP is misconfigured.

## Anti-patterns

| Anti-pattern | Problem | Better approach |
|---|---|---|
| Large trigger-phrase tables | Duplicates built-in routing; consumes context | State the semantic policy only |
| Vague rules | Cannot be verified | Add command, target, and stop condition |
| Substring repository checks | Can match the wrong repository | Compare exact `owner/repository` |
| Repeated rules in several sections | Creates drift and conflicts | Keep one authoritative rule |
| Integration-specific procedures globally | Loaded for unrelated tasks | Move them to a skill |
| Full build for every change | Slow and unnecessary | Run the smallest relevant validation |

---

# Annotated template

```md
# Copilot Instructions

## Scope

<!--
State where these instructions apply.
Describe whether this is a code repo, monorepo, documentation repo,
workspace repo, or coordination repo.
-->

These instructions apply to the entire repository.

## Repository topology

<!--
Describe:
- Repository purpose.
- Source location.
- Test location.
- Documentation location.
- Generated files.
- Related repositories/worktrees.
- Protected paths.
-->

- Purpose: `<purpose>`.
- Source: `<path>`.
- Tests: `<path>`.
- Documentation: `<path>`.
- Generated files: `<path>`.
- Related repository: `<owner/repository>` at `<path>`.

## Mandatory safety rules

<!--
Include only high-impact, objectively verifiable guards.
Define what the agent must do when verification fails.
-->

- MUST verify the repository before commit, push, merge, or PR operations.
- MUST NOT modify `<protected path>`.
- MUST NOT expose credentials, tokens, or `.env` values.
- MUST stop when the target repository or working directory cannot be verified.

## Repository targeting

<!--
Map each action to an exact repository and working directory.
Do not use vague labels such as "code repo" without defining them.
-->

| Action | Repository | Working directory |
|---|---|---|
| Source changes | `<owner/code-repo>` | `<code path>` |
| Build and test | `<owner/code-repo>` | `<code path>` |
| Documentation | `<owner/docs-repo>` | `<docs path>` |
| Issues and planning | `<owner/board-repo>` | `<board path>` |

Before GitHub write operations:

```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

Before Git write operations:

```bash
git rev-parse --show-toplevel
```

## Authoritative sources

<!--
List each source and the information it owns.
Do not list files without explaining why they are authoritative.
-->

- Domain terminology: `<path>`.
- Architecture and decisions: `<path>`.
- API contracts: `<path>`.
- Coding conventions: `<path>`.
- Build instructions: `<path>`.
- Configuration reference: `<path>`.

When documentation and implementation disagree, report the discrepancy.

## Search and code navigation

<!--
Keep the policy short.
Do not reproduce the complete LSP command catalog.
-->

- MUST use LSP first for semantic code navigation.
- MUST use LSP for definitions, references, implementations, call hierarchy, type information, and symbol rename.
- MAY use `rg`, `grep`, or `find` for literals, configuration, generated files, non-code assets, or unsupported LSP queries.
- MUST verify LSP health before fallback caused by missing or incomplete results.
- MUST NOT treat text search as proof of semantic usage.

## Change rules

<!--
Define repository-wide implementation constraints:
- Architecture boundaries.
- Dependency direction.
- Compatibility requirements.
- Generated-code policy.
- Migration requirements.

Move language- or path-specific rules to path-specific instructions.
-->

- MUST preserve `<architectural invariant>`.
- MUST follow `<conventions document>`.
- MUST update tests when behavior changes.
- MUST NOT edit generated files directly.
- SHOULD minimize unrelated changes.

## Build and validation

<!--
Provide tested commands or point to one authoritative build document.
Distinguish targeted validation from full validation.
-->

Follow `<build document>` for supported commands.

Before reporting completion:

1. Inspect the final diff.
2. Run the smallest relevant build.
3. Run tests covering the changed behavior.
4. Run required formatting or lint checks.
5. Report checks not run and why.
6. Confirm no files changed in the wrong repository.

## Documentation rules

<!--
Define:
- Where documentation belongs.
- Required abstraction level.
- ADR/design-document requirements.
- Required cross-references.
-->

- MUST place documentation under `<path>`.
- MUST keep `<high-level document>` free of implementation details.
- MUST record localized decisions under `<ADR path>`.
- MUST cross-reference decisions and affected code.

## Skills and specialized workflows

<!--
Reference skills instead of embedding long conditional workflows.
-->

Use repository skills for specialized tasks:

- `<skill-name>`: `<purpose and trigger>`.

Create skills under:

```text
.github/skills/<skill-name>/SKILL.md
```

Keep large examples, integration procedures, and reference material inside the relevant skill.

## External integrations

<!--
Keep only global integration safety rules here.
Move Jira, Confluence, cloud, deployment, or MCP procedures to skills.
-->

- MUST use configured identifiers instead of guessing them.
- MUST limit broad searches to `<limit>`.
- MUST NOT print or persist secret configuration values.
- MUST report when a required integration is unavailable.

## Completion response

<!--
Define the minimum useful completion report.
-->

Report:

- Files changed.
- Behavior changed.
- Validation performed.
- Validation skipped.
- Remaining risks or follow-up work.
```

## Review checklist

- No contradictory rules.
- No duplicated procedures.
- Every path exists.
- Every command works from the documented directory.
- Repository names use exact identities.
- High-impact rules include verification or stop conditions.
- Specialized workflows live in skills.
- Validation expectations are explicit.
- Secret handling is explicit.
- The file remains useful for nearly every task.

## References

- [GitHub: Adding repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [GitHub: Using LSP servers with Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/lsp-servers)
- [Claude: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [github/awesome-copilot](https://github.com/github/awesome-copilot)
- [dotnet/skills plugins](https://github.com/dotnet/skills/tree/main/plugins)
