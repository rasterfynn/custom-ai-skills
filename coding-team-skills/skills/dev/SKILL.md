---
name: dev
description: Run the dev development team only when the user explicitly selects dev, for example use dev, $dev, or a leading /dev. Do not activate for ordinary coding requests, quoted examples, or another team's name.
---

# dev

Use this skill for the selected top-level task and its follow-ups. Read and follow [the shared development workflow](../coding-teams/references/development-workflow.md) before dispatching work. That workflow is derived from the user's attached general-coding-multi-agents document.

If this skill was inherited by a delegated role, perform the parent's assigned role directly: do not re-enter orchestration, load another team, or create subagents.

## Team roster

| Logical role | Custom agent_type | Model | Reasoning effort |
|---|---|---|---|
| code_mapper | `code_mapper` | `gpt-6.1-sol` | `medium` |
| test_runner | `test_runner` | `gpt-6.1-sol` | `low` |
| architect | `architect` | `gpt-6.1-sol` | `high` |
| docs_researcher | `docs_researcher` | `gpt-6.1-sol` | `high` |
| reviewer | `reviewer` | `gpt-6.1-sol` | `xhigh` |
| implementer | `implementer` | `gpt-6.1-sol` | `low` |

Spawn the exact custom agent types above; their TOMLs pin model and reasoning effort. Preserve the user's chosen team throughout analysis, implementation, review, and testing. A role is a member of the roster, not a requirement to launch all six on every task. Missing role/model support is a reported blocker, not permission to silently switch models or use a generic worker.

If the required workflow reference or exact custom role cannot be loaded, stop and report the blocker. Do not bypass an execution-policy rejection, substitute a direct answer, or claim the team ran.

## Execution

1. Translate the shared workflow's logical roles through this team's roster. Dispatch the relevant read-only analysis questions in parallel and wait for every assigned result.
2. For a requested code change, assign the one implementer after analysis. No coordinator, reviewer, researcher, or test runner edits source/configuration/tests.
3. After implementation, run this team's reviewer and test runner separately in parallel. Route corrections back to the same implementer and repeat only affected verification.
4. For a question, plan, or review-only task, finish the appropriate read-only stages without adding code changes.
5. Collect role reports in the shared five-part format and provide the user's final result with files, verification commands, failures, and remaining risks.

Fast mode inherits the root session's current preference. It is not an agent-local setting. `light` means `low`; `midium` means `medium`. Never downgrade a requested `ultra` setting silently.
