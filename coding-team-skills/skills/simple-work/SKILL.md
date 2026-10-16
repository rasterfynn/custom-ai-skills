---
name: simple-work
description: Delegate a task to exactly one worker with the current parent's model and reasoning effort only when the user explicitly selects simple-work, such as use simple-work, $simple-work, or a leading /simple-work. Do not activate for an unassigned ordinary request, quoted examples, or a discussion of this skill.
---

# Simple work

Use this workflow only when the user actually requests `simple-work`. A delegated agent performs its assigned task directly and must not start this workflow, invoke a dev team, or create further agents.

1. Spawn exactly one custom `single_worker` with a fresh context (`fork_turns="none"` or the host's equivalent). Omit model and reasoning overrides so it inherits the current parent's live model, reasoning effort, and service tier. The role TOML deliberately pins neither model nor effort.
2. Pass the user's actual task, relevant conversation context, constraints, and authorization. Explicitly prohibit nested delegation and team routing. Do not combine a custom agent type with a full-history fork; some Codex versions reject that combination.
3. Do not replace the parent's live selection with saved user defaults or guess an unavailable setting. The supplied installer removes forced personal subagent model/effort defaults. If runtime defaults still override inheritance, explicitly pass the actual live parent values only when known.
4. Wait for this worker and return its result. Reuse that one worker for the same task's follow-ups or corrections. Do not add researchers, reviewers, or test runners unless the user switches to a workflow that calls for them.
5. A question needs an answer, not an invented code change. For authorized changes, the worker performs appropriate focused verification. If the required role or delegation capability is unavailable, report the limitation rather than claiming an agent ran or silently substituting a dev team.

Recognize `use simple-work`, `$simple-work`, and a leading `/simple-work` followed by whitespace or the end of the message. Ignore negated selectors and occurrences only in quoted text, code, attachments, paths, or explanations of the skill. A selector without a task requires clarification before spawning.

Slash-style text is an alias only if the client forwards it to the model; it is not a newly registered built-in command. Prefer `use simple-work` or `$simple-work` when the client intercepts an unknown slash command.

Keep this workflow only for the selected task and its follow-ups. A new independent request without a selected workflow is handled directly by the current agent, with no additional agents. Fast mode inherits the parent session's preference.
