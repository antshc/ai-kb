# Agentic Engineering Concepts

- **Context engineering**  
  Structuring the information an agent receives so it can make better decisions. This includes prompts, retrieved documents, memory, tool outputs, and the current task state.

- **ReAct**  
  A workflow in which the agent alternates between reasoning and acting. It decides what to do, performs an action or uses a tool, then uses the result to guide the next step.

- **Feedback loop**  
  A process in which the agent evaluates the outcome of its actions and adjusts its behavior based on the result. This helps it improve over time instead of repeating the same approach.

- **Chain of thought**  
  The step-by-step reasoning process used to break down complex problems into smaller parts before answering or acting. This is useful for planning, analysis, and problem solving.

- **Installing guardrails**  
  Adding rules, checks, and constraints that keep the agent safe and reliable. Examples include validation, permission controls, policy checks, and approval steps before sensitive actions.

- **Preventing doom loops**  
  Designing the system so the agent does not get stuck repeating the same failed action. Common methods include retry limits, loop detection, timeouts, and fallback behavior.

- **Ralph agent loop**  
  A repeated execution pattern in which an agent works through a task in cycles until the goal is complete. Progress is preserved through external artifacts such as git commits, task files, or logs, so each loop can continue effectively without relying only on live context.

- **Multi-agent coding**  
  Using multiple agents with different responsibilities to solve a coding task together. For example, one agent may write code, another may review it, and another may run tests or validate architecture decisions.

- **State persistence**  
  Saving the agent’s progress, memory, and decisions so it can continue across multiple steps or sessions. This is important for long-running tasks, recovery after failure, and maintaining continuity.

- **Hooks**
Hooks enable automated workflows triggered by specific events during GitHub Copilot coding agent sessions, such as session start, session end, user prompts, and tool usage.

- **HITL (Human In The Loop):** 
A work slice that requires a human decision, review, or approval before it can continue or be completed.

- **AFK (Away From Keyboard):** 
A work slice that can be implemented, tested, and merged automatically without needing human intervention.

- **TL;DR stands for "Too Long; Didn't Read".: ** 
It's internet slang used to introduce a brief summary of a longer text. In context, it means: "to summarize the 'tracer bullets' concept in one sentence — build a small end-to-end slice first, then expand."
