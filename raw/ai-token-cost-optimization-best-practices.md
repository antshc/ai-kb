# AI Token Cost Optimization Best Practices

Reduce total task cost, not prompt length alone. A precise prompt is usually cheaper than retries caused by vague instructions.

## Actionable recommendations

1. **Use the cheapest model that reliably completes the task.**
   Reserve advanced reasoning models for complex debugging, architecture, and ambiguous decisions. Use smaller models for routine implementation, formatting, tests, and summaries.

2. **Define scope and completion criteria.**
   State what must change, what must not change, required validation, and when the agent should stop. This reduces unnecessary exploration and rework.

3. **Start a new session for unrelated tasks.**
   Old messages, tool outputs, and file contents increase every later request. Clear or compact long sessions when prior context is no longer useful.

4. **Provide targeted context.**
   Point to relevant files, symbols, errors, and log ranges instead of supplying entire repositories or documents.

5. **Keep persistent instructions small.**
   Store only recurring repository rules, commands, conventions, and known pitfalls. Persistent instructions are repeatedly added to the context.

6. **Enable only required tools and MCP servers.**
   Tool names, descriptions, and schemas consume context even when the tools are not called.

7. **Preserve prompt-cache prefixes.**
   Put stable instructions, examples, schemas, and tool definitions first; place dynamic request data last. Avoid changing stable prefixes unnecessarily.

8. **Limit output explicitly.**
   Specify the required format, maximum length, and excluded content. Set API output-token limits where available.

9. **Separate research, planning, and implementation.**
   Use a capable model to produce a compact plan, then execute that plan in a fresh session with a cheaper model when appropriate.

10. **Use deterministic validation.**
    Prefer compilers, tests, linters, type checkers, and scanners over additional model reasoning for objective checks.

11. **Measure cost per successful task.**
    Track model, cached and uncached input, output, reasoning tokens, tool calls, retries, and completion success. Optimize workflows using these measurements rather than token count alone.

12. **Batch non-interactive workloads.**
    Use batch APIs for evaluations, classification, embeddings, enrichment, and bulk document processing when immediate results are unnecessary.

13. **Set hard budgets.**
    Configure spend alerts, user quotas, session limits, and request-level token caps to stop runaway usage.

## Recommended priority

1. Route routine tasks to cheaper models.
2. Start fresh sessions between unrelated tasks.
3. Add explicit scope and stopping conditions.
4. Limit output length.
5. Reduce enabled tools.
6. Preserve cache-compatible prompt prefixes.
7. Measure cost per successfully completed task.

## Sources

- [GitHub Copilot: Optimize AI usage](https://docs.github.com/en/copilot/tutorials/optimize-ai-usage)
- [GitHub Copilot CLI: Context management](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management)
- [OpenAI: Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI: Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization)
- [OpenAI: Batch API](https://developers.openai.com/api/docs/guides/batch)
- [Anthropic: Token counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting)
