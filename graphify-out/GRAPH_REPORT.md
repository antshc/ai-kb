# Graph Report - graphify-out  (2026-07-27)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 153 nodes · 183 edges · 22 communities (15 shown, 7 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be2cadd7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21

## God Nodes (most connected - your core abstractions)
1. `Upwork AI Buyers and What a Senior Developer Can Sell Them` - 10 edges
2. `CLAUDE.md Template` - 9 edges
3. `Durable State Machine` - 8 edges
4. `Glossary — Building Great Skills` - 8 edges
5. `Copilot Instructions` - 8 edges
6. `handoff.md Template` - 7 edges
7. `Claude Agent Template Pack` - 7 edges
8. `workflow.yaml` - 6 edges
9. `Agent Skill Plugin Authoring Standard` - 6 edges
10. `Lines of Inquiry → Probes → Coverage Checklist` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Sequential Flow` --semantically_similar_to--> `workflow.yaml`  [INFERRED] [semantically similar]
  D:/_projects/ai-kb/raw/agent-patterns.md → D:/_projects/ai-kb/raw/custom-skill-workflow-yaml.md
- `Ralph Agent Loop` --semantically_similar_to--> `Durable State Machine`  [INFERRED] [semantically similar]
  D:/_projects/ai-kb/raw/agentic-engineering-concepts.md → D:/_projects/ai-kb/raw/improve-agent-robustness-and-resumability.md
- `Atomic Task Tracker` --semantically_similar_to--> `Coverage Checklist`  [INFERRED] [semantically similar]
  D:/_projects/ai-kb/raw/state-persistence-template-tasks.md → D:/_projects/ai-kb/raw/skills-lines-of-inquiry-probes-checklist.md
- `Operator Pattern` --semantically_similar_to--> `Workflow Agent`  [INFERRED] [semantically similar]
  D:/_projects/ai-kb/raw/agent-patterns.md → D:/_projects/ai-kb/raw/ai-agents-skills-bussines-areas-deep-research-report.md
- `Split & Merge Pattern` --semantically_similar_to--> `Multi-Agent Coding`  [INFERRED] [semantically similar]
  D:/_projects/ai-kb/raw/agent-patterns.md → D:/_projects/ai-kb/raw/agentic-engineering-concepts.md

## Hyperedges (group relationships)
- **Custom Skill Workflow Artifacts** — raw_custom_skill_workflow_yaml_workflow_yaml, raw_custom_skill_workflow_yaml_skill_md, raw_custom_skill_workflow_yaml_workflow_schema_json, raw_custom_skill_workflow_yaml_runtime_state, raw_custom_skill_workflow_yaml_machine_readable_workflow_contract [EXTRACTED 1.00]
- **Durable Execution State Model** — raw_improve_agent_robustness_and_resumability_durable_state_machine, raw_improve_agent_robustness_and_resumability_invocation_scoped_durable_state, raw_improve_agent_robustness_and_resumability_task_fingerprint, raw_improve_agent_robustness_and_resumability_explicit_phase_outcomes, raw_improve_agent_robustness_and_resumability_skill_call_checkpointing, raw_improve_agent_robustness_and_resumability_verification_receipts, raw_improve_agent_robustness_and_resumability_finalization_completeness_sweep [EXTRACTED 1.00]
- **Agent Architecture Patterns** — raw_ai_agents_skills_bussines_areas_deep_research_report_retrieval_grounded_copilot, raw_ai_agents_skills_bussines_areas_deep_research_report_workflow_agent, raw_ai_agents_skills_bussines_areas_deep_research_report_batch_analytics_agent, raw_ai_agents_skills_bussines_areas_deep_research_report_retrieve_reason_plan_act_verify_commit_log [EXTRACTED 1.00]
- **Grill-Design Interview Pattern** — raw_skills_lines_of_inquiry_probes_checklist_lines_of_inquiry, raw_skills_lines_of_inquiry_probes_checklist_probes, raw_skills_lines_of_inquiry_probes_checklist_coverage_checklist [EXTRACTED 1.00]
- **Claude State Persistence Pack** — raw_state_persistence_template_claude_claude_md_template, raw_state_persistence_template_tasks_tasks_template, raw_state_persistence_template_progress_progress_template, raw_state_persistence_template_claude_handoff_handoff_template, raw_state_persistence_template_claude_failures_failures_template, raw_state_persistence_template_claude_results_st_001_st_001_example_result [EXTRACTED 1.00]
- **Vertical Slice Principles** — raw_vertical_slices_archutecture_copilot_instructions_vertical_slice_architecture, raw_vertical_slices_archutecture_copilot_instructions_feature_first_organization, raw_vertical_slices_archutecture_copilot_instructions_thin_endpoints, raw_vertical_slices_archutecture_copilot_instructions_focused_handlers, raw_vertical_slices_archutecture_copilot_instructions_isolated_infrastructure, raw_vertical_slices_archutecture_copilot_instructions_explicit_code_over_premature_abstraction [EXTRACTED 1.00]

## Communities (22 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (23): Sequential Flow, Machine-Readable Workflow Contract, SKILL.md, workflow.schema.json, workflow.yaml, LSP-First Navigation, Normative Vocabulary, Progressive Disclosure (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (23): Agentic Tool-Calling Retrieval, Parallel Independent Retrieval, Precision-First Tool Ordering, Progressive Disclosure, RAG Cheat Sheet for Claude Code / Copilot-style Agents, Glossary — Building Great Skills, Cognitive Load, Completion Criterion (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (16): CLAUDE.md Template, Anti-Doom-Loop Memory, failures.md Template, handoff.md Template, Restart Instructions, Persistent Project Rules, Completed Task Output, ST-001 Example Result (+8 more)

### Community 3 - "Community 3"
Cohesion: 0.36
Nodes (11): Coverage Checklist, Inline Capture Step, Lines of Inquiry, Lines of Inquiry → Probes → Coverage Checklist, Not Applicable with Reason, Probes, Coverage Checklist, Grill Design (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (11): AI Automation POC, High-Probability Upwork Buyer Sectors, Production ML Deployment + Monitoring Starter, Productized Outcome-First Offerings, RAG Audit + Hardening, RAG MVP, Two-Step Close, Upwork AI Buyers and What a Senior Developer Can Sell Them (+3 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (10): Ralph Agent Loop, State Persistence, Workflow Orchestration vs Open-Ended Agents, Runtime State, Durable State Machine, Explicit Phase Outcomes, Finalization Completeness Sweep, Invocation-Scoped Durable State (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.42
Nodes (9): Async by Default, Business Rule Policy / Calculator Classes, Copilot Instructions, Explicit Code over Premature Abstraction, Feature-First Organization, Focused Handlers, Isolated Infrastructure, Thin Endpoints (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (8): Operator Pattern, Agent Harness, HITL, Human-in-the-Loop Copilot + Workflow Agents, Retrieval-Grounded Copilot, Workflow Agent, Grounded Generation (RAG), Tool Calling and Controlled Execution Loops

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (8): ILoyaltyDiscountCalculator, Loyalty Discount Design Decision, LoyaltyDiscountCalculator, OrderPricingService.CalculateTotals, BCryptPasswordHasher, IPasswordHasher, Password Security Design Decision, UserRegistrationService.RegisterAsync

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (7): ReAct, Batch Analytics Agent, Deterministic Tools, Model Context Protocol, Programmatic Tool Calling, Retrieve Reason Plan Act Verify Commit Log, Standardized Connectors for Tools and Data

### Community 10 - "Community 10"
Cohesion: 0.50
Nodes (5): Context in a Design Document, Current State, Goals, Non-Goals, Problem

### Community 11 - "Community 11"
Cohesion: 0.50
Nodes (4): Installing Guardrails, AI RMF, OWASP LLM Risks, Security and Governance-by-Design

### Community 12 - "Community 12"
Cohesion: 0.83
Nodes (4): AC + Decision Formula, Acceptance Criterion to Subtask Mapping, Implementation Anchor, Spec → Design → Task: Mapping Guide

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (3): Agent Teams Pattern, Split & Merge Pattern, Multi-Agent Coding

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (3): A/B Testing Templates, Implementation Roadmap, Metric Stack

## Knowledge Gaps
- **37 isolated node(s):** `HITL`, `AFK`, `Agent Harness`, `OWASP LLM Risks`, `AI RMF` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Durable State Machine` connect `Community 5` to `Community 0`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **What connects `HITL`, `AFK`, `Agent Harness` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.10276679841897234 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10276679841897234 - nodes in this community are weakly interconnected._