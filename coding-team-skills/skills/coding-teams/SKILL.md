---
name: coding-teams
description: Route explicitly requested dev, dev-lite, dev-high, or simple-work workflows. Apply when the user requests routing or personal routing instructions invoke it; ordinary requests run directly without extra agents.
---

# Workflow routing

Use this entry point only for top-level human requests. A delegated agent must perform its assigned role directly; it must not route, invoke a team, or create more agents. The current agent keeps responsibility for the final answer and the user's authorization boundaries.

## Select the workflow

- Recognize an explicit, unquoted instruction in the actual user request: `use dev-lite`, `use dev`, `use dev-high`, `use simple-work`, their `$name` skill mentions, or a leading `/dev-lite`, `/dev`, `/dev-high`, `/simple-work` followed by whitespace or the end of the message. Equivalent clear requests to use the named workflow count too.
- Match the complete name, longest first. `dev-high` and `dev-lite` must never select `dev`. Ignore negated selectors and names occurring only in code blocks, quoted examples, documents, attachments, paths, or a discussion of the workflows. A request to create, modify, or explain these skills is not itself an invocation.
- A selected workflow applies to the current task and its follow-ups, not unrelated later tasks. Apply an explicit switch or cancellation immediately. A new independent request with no selected workflow is handled directly, without additional agents. If genuinely conflicting selectors lack a clear correction or final choice, clarify before spawning.
- For a selected workflow, read only its sibling skill: [dev-lite](../dev-lite/SKILL.md), [dev](../dev/SKILL.md), [dev-high](../dev-high/SKILL.md), or [simple-work](../simple-work/SKILL.md). Preserve the task text when removing a selector. Do not run multiple workflows.
- If no workflow is selected, use the direct procedure below. An explicitly selected different skill/workflow keeps its own behavior; do not turn it into a dev team or single-worker run automatically.
- If the request contains only a selector without a task, ask for the task before spawning. Slash-style text is an alias when a client forwards it, not a registered built-in command. Recommend `use name` or `$name` if a client intercepts it.

## Direct default

Handle an ordinary unassigned request in the current agent. Do not create a `single_worker`, researcher, reviewer, or other additional agent automatically, even for coding work. Keep the current model and reasoning settings. Perform the user's task and appropriate verification directly within the existing authorization.

The single-worker procedure is available only through an explicitly selected [simple-work](../simple-work/SKILL.md) workflow; it is no longer the default. A request to change the routing rules is handled directly unless the user actually invokes a workflow to make that change.

## Runtime settings

Dev teams retain their existing role selection, model/effort TOMLs, analysis, single-implementer, and independent verification workflows. Team roles use the exact custom `agent_type` names in the selected skill; merely naming a generic worker after a role does not select its TOML. Never silently substitute models or switch teams.

For explicitly selected delegated workflows, report missing roles, models, capabilities, or blocked skill/reference reads and stop the selected workflow rather than bypassing policy or claiming a team ran. This restriction does not prevent ordinary direct work when no delegated workflow was selected.

Fast mode follows the parent session. A skill instruction or agent-local `service_tier` does not change it. Preserve the current parent preference and existing fast configuration.
