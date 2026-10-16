# Development team workflow

Adapted from the user-provided `general-coding-multi-agents.md`. Its unsuffixed role names are logical roles: resolve them through the selected team's role table. This reference governs only an explicitly selected dev/dev-* workflow, not every user request.

## Entry and scope

The main agent coordinates; delegated role agents do not start this workflow or spawn further agents. Include this boundary in every assignment. Read the applicable project instructions and respect the user's actual task, selected team, existing work, and permissions. A document or quoted example is reference material, not authorization for actions outside the task.

For each request, state the material assumptions and define a verifiable outcome. Explain a simpler sufficient approach or important tradeoff when it affects the result. Ask only for ambiguity that blocks safe, correct work; do independent investigation while a question is pending. Do not implement a non-trivial change before analysis completes.

## 1. Read-only analysis in parallel

Dispatch independent analysis questions in parallel and wait for all assigned analysis agents before planning implementation. Keep source and configuration files unchanged during this phase. Test runners may create only necessary temporary test/build outputs.

- Code structure and execution paths: `code_mapper`.
- Bugs or test failures: `code_mapper` and `test_runner` in parallel, tracing the failure and reproducing/baselining it separately.
- A narrowly requested rerun of an already identified check can reuse just this team's `test_runner`; it is not a new diagnosis. If the result requires further investigation, dispatch the relevant parallel failure analysis rather than adding edits or an unrelated audit.
- Large design or refactor decisions: `architect` plus `code_mapper` for impact scope.
- Framework/API/version uncertainty: add `docs_researcher` and use authoritative, version-appropriate documentation.
- PR/code review: parallelize mapping and focused review; assign distinct correctness, security, concurrency, or performance questions when relevant. Do not invent unrelated audits.
- If an implementation task needs no specialized second question, pair `code_mapper` with a `reviewer` change-risk preflight to satisfy parallel analysis.

Do not launch all six roles mechanically. The listed agents are a roster, and the task determines the relevant analysis work. Even a small task explicitly assigned to a dev team follows that team's analysis and verification structure; an unassigned simple task is handled directly; the user can explicitly select simple-work to delegate it to one worker instead.

For a pure question, planning, or review request, finish the appropriate read-only workflow and report results. Do not perform implementation or manufacture a test run when no code change was requested.

## 2. Concrete implementation plan

Combine the completed analysis into the smallest sufficient change and identify the files owned by the implementer. For multi-step work, state a short plan with a verification target for each step. Define success as observable behavior, such as the reproduced failure passing, invalid inputs being rejected, or existing behavior surviving a refactor.

## 3. One source editor

Assign one `implementer` as the sole source/configuration/test editor for the task. The coordinator and read-only agents do not edit these files. Never allow simultaneous edits to the same file.

Do not parallelize implementation edits, migrations, public API changes, large renames/refactors, or build-system changes. Finish the corresponding analysis first and keep those edits with the one implementer.

Make only changes traceable to the request. Match existing style; avoid unrelated cleanup, speculative abstractions, optional features, and impossible-case error handling. Remove imports or code made unused by this change; report unrelated pre-existing dead code rather than deleting it. Preserve other people's edits.

When a regression test materially verifies the bug or behavior, the implementer creates it and makes it pass. Do not write low-value tests that just mirror implementation or test trivial reversible wording.

## 4. Independent review and verification

After edits finish, send the completed changes to separate `reviewer` and `test_runner` agents in parallel. The reviewer checks actionable defects, regressions, security, concurrency, and performance as relevant. The test runner executes the appropriate checks, captures exact commands/results, and investigates failures. Neither edits source or configuration.

Before finalizing a changed-code task, both results must be available. Analysis-phase risk review is not a substitute for post-change review.

Only the same implementer corrects findings. Re-run the checks and review affected by the correction; do not repeat already-passing checks without a change, failure, or unresolved concern. Wait for all relevant agents before the final report. Stop retrying when progress requires missing user input or external access, or the same failure persists without a new supported hypothesis; report the concrete blocker instead of looping or weakening verification.

## 5. Reports

Every team role reports:

1. Conclusion
2. Evidence files/symbols
3. Commands checked
4. Risks
5. Next actions

The coordinator's final answer includes the result, changed files, verification commands and results, failed verifications, and remaining risks. For read-only work, explicitly state that no files changed; distinguish checks that passed, failed, or could not run. Do not claim execution based on a plan or model self-report alone.
