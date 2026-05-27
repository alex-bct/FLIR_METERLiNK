# Jira Project Config

Fill this file with the actual Jira settings for the project before using write operations in production.

## Connection

- Jira base URL: `https://dt360.atlassian.net`
- Preferred access method: `direct REST`
- Auth method: `API token`
- Credential source: `JIRA_BASE_URL`, `JIRA_USER_EMAIL`, `JIRA_API_TOKEN`
- Auth header format: `Authorization: Basic <base64(email:api_token)>`

## Project Scope

- Default project key: `GBS`
- Additional project keys used by this workspace: `[TODO]`
- Default issue types: `[TODO: Task / Story / Bug / Sub-task / Epic]`
- Default parent or epic rules: `[TODO]`

## Required Fields For Create

List every required field and the expected value source.

| Field | Jira name or ID | Required? | Default / rule |
| --- | --- | --- | --- |
| Summary | summary | yes | concise action-oriented title |
| Description | description | yes/no | use structured template |
| Issue type | issuetype | yes | derive from user request |
| Assignee | `[TODO]` | `[TODO]` | `[TODO]` |
| Priority | `[TODO]` | `[TODO]` | `[TODO]` |
| Epic link / parent | `[TODO]` | `[TODO]` | `[TODO]` |

Add project custom fields below as needed.

| Field purpose | Jira name or ID | Required? | Notes |
| --- | --- | --- | --- |
| `[TODO]` | `[TODO]` | `[TODO]` | `[TODO]` |

## Valid Workflow States

Document the exact workflow names used by the project.

- Backlog: `[TODO]`
- To Do: `[TODO]`
- In Progress: `[TODO]`
- In Review: `[TODO]`
- QA / UAT: `[TODO]`
- Done: `[TODO]`
- Blocked: `[TODO]`

## Transition Rules

- Required fields during transition: `[TODO]`
- States that require comments: `[TODO]`
- States that should never be set without confirmation: `[TODO]`

## Comment Conventions

- Standup/progress format: `[TODO]`
- QA finding format: `[TODO]`
- Stakeholder update format: `[TODO]`

## Naming And Content Rules

- Summary style: `[TODO]`
- Description template expectations: `[TODO]`
- Labels/components conventions: `[TODO]`
- Linked issue conventions: `[TODO]`

## Safe Defaults

Until this file is completed:
- allow read operations if credentials exist
- require confirmation for create, update, comment, and transition actions
- do not guess custom fields or transition names

## Current Known Values

- Jira base URL env var: `JIRA_BASE_URL`
- Jira user email env var: `JIRA_USER_EMAIL`
- Jira API token env var: `JIRA_API_TOKEN`
- Known user account: `your.email@company.com`
- Suggested local template in this workspace: `.env.jira.example`

## Known Working API Pattern

Another working integration in this environment uses Jira Cloud Basic Authentication with:

- email: `your.email@company.com`
- token source: Atlassian API token
- header: `Authorization: Basic <base64(email:token)>`

Known working endpoints:

- Read plain-text style fields with API v2:
  `GET /rest/api/2/issue/GEI-328?fields=summary,description`
- Read rich-text issue payload with API v3:
  `GET /rest/api/3/issue/GEI-328`

When troubleshooting, prefer testing a known issue endpoint first before account-level or board-level endpoints, because another integration has already proven that issue-level access works with this pattern.
