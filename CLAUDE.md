<!--
  AUTO-GENERATED FROM config.yaml.
  Do not edit by hand. Re-run: node mcp-server/src/generate-claude-md.js
  Source of truth: humonex-ai/dev-standards
-->

# Humonex Dev Workflow Rules

You are working inside a Humonex project. The workflow below is **enforced by tools**, not by manners. Every rule here is backed by the `humonex-dev-standards` MCP server.

Task management runs on **GitHub Projects (org-level Project v2)**. Every Issue lives on the `humonex-ai` org-level Project #4.

## Hard Rules

- **session_start_required** — Always call session_start before any work — no exceptions.
- **no_direct_commits_to_protected** — Never commit to main, uat, or dev directly.
- **branch_naming** — Branch name must follow the configured pattern and include the GitHub issue number.
- **session_end_required** — Always call session_end when done.
- **out_of_scope_work** — If work falls outside the current task, create a new GitHub issue first via create_task.
- **pr_via_mcp_only** — Always generate PRs via create_pr — never manually.
- **definition_of_done_required** — Ask for Definition of Done before starting any task.

## How to Start Work

Before touching any code, call:

```
session_start({
  task_id: "<42>"  | "<repo#42>" | "<owner/repo#42>",
  description: "<short kebab phrase>",
  work_type: "feature" | "bugfix" | "hotfix" | "chore",
  definition_of_done: "<what done looks like>"
})
```

This:
- Resolves the GitHub Issue in `humonex-ai`
- Creates the correctly-named branch from the configured base
- Moves the org Project card to **In Progress**
- Captures the Definition of Done as the first comment on the Issue

**Definition of Done is required.** What does done look like for this task?

## Branch Naming

Pattern: `{type}/{task_id}-{description}`

`{task_id}` = the GitHub Issue number (numeric).

Allowed types: `feature`, `bugfix`, `hotfix`, `chore`

Description: lowercase kebab, max 6 words. Task id is mandatory.

Examples:
- `feature/42-user-profile-page`
- `bugfix/31-avatar-upload-crash`
- `hotfix/55-critical-login-fix`
- `chore/23-update-readme`

## Protected Branches

Never commit directly to: `main`, `uat`, `dev`.

All work merges in via PR.

## Environments

| Environment | Branch | Approvals |
|---|---|---|
| development | `dev` | 1 |
| uat | `uat` | 1 |
| production | `main` | 2 — PM approval required |

Branches cut from:
- `feature` → `dev`
- `bugfix` → `dev`
- `hotfix` → `main`
- `chore` → `dev`

## Workflow States (org Project Status field)

1. Backlog
2. In Sprint
3. In Progress
4. In Review
5. Done

State transitions (automatic — do not move manually):
- Session start → **In Progress**
- PR opened → **In Review**
- PR merged to `dev` → **Done**
- PR merged to `main` → tagged **Released**

## Mid-Session Discoveries

If you find work that is **not part of the current task**, do not silently expand scope.

- Bug? → `create_task({ kind: "bug", title, priority: "High" })`
- New task? → `create_task({ kind: "task", title })`

Both land in **Backlog** so the PM can triage before the next sprint.

## Finishing Work

```
session_end({
  summary: "<what was done>",
  remaining_work: "<optional, what's left>",
  completed: true | false
})
```

Comment posted to the GitHub Issue includes: developer name, session start time, session end time, branch name, commit ids, commit messages, files changed, summary, remaining work, pr link, definition of done.

## Opening a PR

PRs are **always** opened through the MCP tool — never manually.

```
create_pr({
  target_environment: "development" | "uat" | "production",
  body: "<summary that fills the PR template>"
})
```

PR body includes a `Closes #N` line so the Issue auto-closes on merge.

Required PR sections: `Summary`, `Task`, `Changes`, `Testing`, `Screenshots`.

After the PR opens:
- Link posted as a comment on the Issue
- org Project card moves to **In Review**

## Listing Your Work

- Sprint tasks → `list_tasks()`
- QA-raised bugs → `get_bugs()`

## What Will Get You Blocked

- Committing on `main`, `uat`, `dev` — push is rejected, PR cannot open against the wrong base
- Branch name missing the GitHub Issue number — `session_start` refuses
- Description over 6 words — refused
- Skipping Definition of Done when required — refused
- Raising a PR with required sections missing — refused

---

_Source: `humonex-ai/dev-standards/config.yaml` (version 2, last updated Fri May 15 2026 05:30:00 GMT+0530 (India Standard Time))._
