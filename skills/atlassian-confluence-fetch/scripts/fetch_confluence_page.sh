#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <PAGE_ID> [OUTPUT_DIR]" >&2
  exit 2
fi

if [[ -z "${ATLASSIAN_SITE:-}" || -z "${ATLASSIAN_EMAIL:-}" || -z "${ATLASSIAN_TOKEN:-}" ]]; then
  echo "Missing required env vars. Please set ATLASSIAN_SITE, ATLASSIAN_EMAIL, ATLASSIAN_TOKEN." >&2
  exit 2
fi

PAGE_ID="$1"
OUT_DIR="${2:-artifacts/confluence}"

if ! [[ "$PAGE_ID" =~ ^[0-9]+$ ]]; then
  echo "PAGE_ID must be numeric: $PAGE_ID" >&2
  exit 2
fi

mkdir -p "$OUT_DIR"
RAW_JSON="$OUT_DIR/$PAGE_ID.raw.json"
MD_OUT="$OUT_DIR/$PAGE_ID.md"

URL="https://${ATLASSIAN_SITE}/wiki/rest/api/content/${PAGE_ID}?expand=body.storage,version,space"

curl -fsS --user "${ATLASSIAN_EMAIL}:${ATLASSIAN_TOKEN}" "$URL" -o "$RAW_JSON"

python3 "skills/atlassian-confluence-fetch/scripts/storage_to_markdown.py" "$RAW_JSON" "$MD_OUT"

echo "Fetched page ${PAGE_ID}"
echo "Raw JSON: ${RAW_JSON}"
echo "Markdown: ${MD_OUT}"
