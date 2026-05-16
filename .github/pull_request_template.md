<!--
  Humonex PR template.

  Two ways this file gets used:
  1. Rendered by `create_pr` in the MCP server. The placeholders below
     (in double curly braces) are filled with session data, and a
     `Closes #N` line is prepended so the GitHub Issue auto-closes
     when the PR merges.
  2. Copied into each project repo as `.github/pull_request_template.md`
     (done by install.sh) so manually-opened PRs still get the same shape.

  Required sections (validated by the MCP tool against pull_requests.required_sections):
    Summary, Task, Changes, Testing, Screenshots

  Do not rename a section heading without updating config.yaml.
-->

## Summary

{{summary}}

## Task

- Issue: **{{task_id}}** ({{issue_url}})
- Branch: `{{branch}}`

## Definition of Done

{{definition_of_done}}

## Changes

<!-- Bullet what changed at a code level. One bullet per logical change.
     Example:
     - Added `AvatarUpload` size guard (rejects >2MB before upload)
     - Wired `ProfilePage` form to `PATCH /users/me`
-->

- _TBD_

## Testing

<!-- How a reviewer can verify this. Include commands, manual steps, and
     environments touched. Anything not tested goes under "Not tested". -->

**Steps to verify:**

- _TBD_

**Not tested:**

- _TBD_

## Screenshots

<!-- UI-affecting PRs: before/after screenshots or a short clip.
     Backend-only PRs: write "N/A". The section must exist either way. -->

_N/A_

## Checklist

- [ ] Branch follows naming convention (`{type}/{ISSUE_NUMBER}-{description}`)
- [ ] org Project card is in **In Review** (auto-moved by MCP / gh-sync)
- [ ] Definition of Done above matches what was agreed at session start
- [ ] No direct commits to `main`, `uat`, or `dev`
- [ ] PR targets the correct environment branch
