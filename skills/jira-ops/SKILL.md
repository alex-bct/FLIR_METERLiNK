---
name: jira-ops
description: Use this skill when working with Jira issues for a project, especially to read issue details, create new issues, update fields, add comments, or move issues through workflow transitions. Use it when the user asks to inspect a ticket, create a ticket from requirements, modify status or fields, or sync project work into Jira safely.
---

# Jira Ops

## Overview

This skill helps Codex handle Jira issue operations safely and consistently: read existing tickets, create new tickets, update issue fields, add comments, and perform workflow transitions.

Prefer this skill whenever the user asks for Jira work in natural language and the task may involve project-specific rules such as required fields, issue types, naming conventions, or approval boundaries.

## Quick Start

1. Identify the requested action: `read`, `create`, `update`, `comment`, or `transition`.
2. Load [references/project-config.md](references/project-config.md) before any write action, and also before read actions if project-specific ticket keys, fields, or terminology matter.
3. Prefer Jira Cloud Basic Auth with environment variables:
   - `JIRA_BASE_URL`
   - `JIRA_USER_EMAIL`
   - `JIRA_API_TOKEN`
4. If the current workspace contains a local Jira env file, prefer `.env.jira`. Use `.env.jira.example` only as a template.
5. If no access path or credentials are available, stop and report exactly what is missing.
6. For write actions, summarize the intended changes before execution when the request is ambiguous or high-impact.
7. After execution, report the ticket key, the fields changed, and any follow-up actions still needed.

## Operating Rules

- Never invent Jira field IDs, transition IDs, or custom field names when they can be discovered from project configuration or the Jira API.
- Do not modify destructive or high-impact fields silently. Examples: assignee, priority, sprint, labels used for automation, workflow status, fix version, or custom approval fields.
- If the user asks for a vague update such as "幫我改一下", first resolve the exact target field and desired value.
- Preserve existing ticket context. When updating description-style fields, merge carefully instead of overwriting useful content unless the user explicitly wants replacement.
- Prefer idempotent reads before writes: fetch the current issue first, then compute the minimal change.
- When a requested change conflicts with workflow rules or missing required fields, explain the blocker and propose the smallest next step.

## Task Workflows

### Read an issue

Use this when the user asks to inspect a ticket, summarize it, list comments, or compare current state.

Checklist:
- Resolve the issue key.
- Fetch core fields at minimum: summary, description, issue type, status, assignee, reporter, priority, labels, linked issues, comments, and any project-required custom fields.
- If the user wants a summary, present the current state plus important risks, blockers, and next actions.
- If the issue is not found, verify the project key format before reporting failure.

### Create an issue

Use this when the user provides a bug, task, story, change request, or meeting outcome that should become a ticket.

Checklist:
- Determine project key and issue type.
- Build a concise summary and a structured description.
- Populate required defaults from [references/project-config.md](references/project-config.md).
- Include acceptance criteria, reproduction steps, or business impact when available.
- Before creation, verify required fields and parent/epic linkage if applicable.
- After creation, return the new issue key and the fields that were set.

Suggested description shape:
- Background
- Problem or request
- Scope
- Acceptance criteria
- Notes or dependencies

### Update an issue

Use this when the user wants to change fields on an existing ticket.

Checklist:
- Read the current issue first.
- Identify the exact fields to change.
- Preserve unrelated fields.
- If updating description or long text, produce a diff-style summary in the response.
- Re-fetch the issue after updating when the API response does not already confirm the final state.

Common updates:
- summary or description edits
- assignee changes
- priority or labels
- due date, sprint, epic link, fix version
- custom project fields

### Add a comment

Use this when the user wants to leave progress notes, QA findings, questions, or stakeholder updates.

Checklist:
- Keep comments concise and action-oriented.
- Mention blockers, decisions, and next steps.
- Avoid duplicating the full ticket description in comments.
- If the project has a comment format, follow it from [references/project-config.md](references/project-config.md).

### Transition workflow status

Use this when the user asks to move a ticket between statuses such as `To Do`, `In Progress`, `In Review`, `Done`, or project-specific states.

Checklist:
- Discover the valid transitions for the current issue.
- Verify whether additional required fields must be set during the transition.
- If multiple similar target statuses exist, use the exact configured one from Jira rather than guessing.
- Report both the previous and new status.

## Field Mapping Guidance

When the project uses custom fields, read [references/project-config.md](references/project-config.md) and map user language into the real Jira fields.

Examples:
- "幫我補負責人" -> assignee
- "改成高優先" -> priority
- "補上測試結果" -> comment or a QA custom field depending on project rules
- "移到待驗收" -> workflow transition, not a plain status field edit

When unsure whether a request is a field update or a transition, treat it as a transition question and inspect available transitions first.

## Response Pattern

For read requests, respond with:
- issue key and summary
- current status and owner
- the requested details
- important blockers or next steps

For write requests, respond with:
- issue key
- operation performed
- exact fields or status changed
- any validation warnings or missing follow-up

## Resource Use

Read [references/project-config.md](references/project-config.md) for project-specific Jira details before doing concrete work. Keep SKILL.md generic and store project-specific values only in that reference file.

If a workspace provides a Jira env template such as `.env.jira.example`, instruct the user to copy it to a real env file and fill in `JIRA_API_TOKEN` locally rather than pasting secrets into chat.
