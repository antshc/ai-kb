---
title: Custom Skill workflow.yaml
source_document: sources/custom-skill-workflow-yaml-md-ff35138ed3f511a1
tags: [summary]
---

# Custom Skill workflow.yaml

**Source:** sources/custom-skill-workflow-yaml.md

## Overview

This document explains the role and proper use of `workflow.yaml` in GitHub Copilot and Claude Agent Skills. `workflow.yaml` is not a standard executable; it is a custom machine-readable workflow contract used alongside `SKILL.md`. The document covers recommended structure, responsibility split, validation rules, execution model, and when to use or avoid `workflow.yaml`.

## Key Claims

- [[skill.md]] uses [[workflow.yaml]] (confidence: 0.95)
- [[workflow-interpreter]] reads from [[workflow.yaml]] (confidence: 0.9)
- [[workflow-interpreter]] uses [[success-gate]] (confidence: 0.9)
- [[success-gate]] causes [[failure-policy]] (confidence: 0.85)
- [[workflow.yaml]] contains [[workflow-phase]] (confidence: 0.95)
- [[agent-skill]] uses [[skill.md]] (confidence: 0.95)
- [[github-copilot]] uses [[agent-skill]] (confidence: 0.9)

## Entities

- [[workflow.yaml]] (component)
- [[skill.md]] (component)
- [[github-copilot]] (software)
- [[agent-skill]] (concept)
- [[workflow-phase]] (process)
- [[workflow-schema]] (component)
- [[workflow-interpreter]] (software)
- [[success-gate]] (process)
- [[failure-policy]] (concept)
- [[github-actions-workflow]] (process)
- [[agentic-workflow]] (process)
- [[runtime-state]] (concept)

## Open Questions

- When is it appropriate to split a skill into multiple specialized skills instead of using workflow.yaml phases?
