# Personal workflow routing

Apply these rules to top-level human requests only. If you are a delegated agent, perform the assigned task directly; do not route, start a workflow, or create more agents.

With no explicitly selected workflow, handle the user's request directly in the current agent. Do not automatically create a single worker or any additional research, review, or implementation agents. This direct mode is the default for questions and coding tasks alike.

Preserve the existing `dev-lite`, `dev`, and `dev-high` workflows when the user selects one. Recognize `use dev-lite`, `use dev`, `use dev-high`, the corresponding `$name` skill mentions, and leading slash-style selectors when delivered as message text. Read the selected skill under `skills/` relative to this Codex home directory.

Only when the user explicitly selects `simple-work` (for example `use simple-work`, `$simple-work`, or leading `/simple-work`), read `skills/simple-work/SKILL.md` and delegate to exactly one custom `single_worker` with a fresh context (`fork_turns="none"` or equivalent). Omit model and reasoning overrides so it inherits the current parent's live model, reasoning effort, and service tier; forward the task and relevant context, prohibit nested delegation, wait, and return its result. Do not combine a custom agent type with a full-history fork.

Match complete workflow names, longest first. Ignore negated selectors and quoted/document/example references. A request to create, modify, or explain these workflows is not itself an invocation. For detailed selection rules, read `skills/coding-teams/SKILL.md` relative to this Codex home directory.

Retain a selected workflow only for that task's follow-ups, including dev-team follow-ups. Respect an explicit switch or cancellation. A new unrelated request without a selector returns to direct handling with no additional agents. An explicitly selected different skill/workflow keeps its own behavior.

If an explicitly selected delegated workflow or required role cannot be loaded, report its concrete blocker rather than substituting another workflow or claiming an agent ran. This does not block direct handling when no delegated workflow was selected.

Permissions and higher-priority instructions still apply. Workflow selection does not authorize unrelated external actions. Never substitute fixed or stale saved defaults for the user's current model selection in `simple-work`.
