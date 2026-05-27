---
name: atlassian-confluence-fetch
description: Fetch and normalize private Atlassian Confluence pages using local environment credentials. Use when a user provides a Confluence URL or page id and asks to retrieve spec content without sharing tokens in chat.
---

# Atlassian Confluence Fetch

Use this skill when the user wants content from a private Confluence page.

## Safety Rules

- Never ask the user to paste API tokens in chat.
- Read credentials only from local environment variables:
  - `ATLASSIAN_SITE` (example: `dt360.atlassian.net`)
  - `ATLASSIAN_EMAIL`
  - `ATLASSIAN_TOKEN`

## Workflow

1. Resolve page id.
- If input is a URL like `/pages/3993567233/...`, extract `3993567233`.
- If input is already numeric, use it directly.

2. Fetch and normalize with bundled script.
- Run:
  - `bash skills/atlassian-confluence-fetch/scripts/fetch_confluence_page.sh <PAGE_ID>`

3. Read generated output and continue the user task.
- Raw JSON is written to:
  - `artifacts/confluence/<PAGE_ID>.raw.json`
- Normalized text markdown is written to:
  - `artifacts/confluence/<PAGE_ID>.md`

## Notes

- If fetch fails with `401/403`, tell the user to refresh token permission or site scope.
- If the page has macros/complex tables, raw JSON remains available for deeper parsing.
