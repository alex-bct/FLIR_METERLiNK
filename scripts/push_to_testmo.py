#!/usr/bin/env python3
"""
push_to_testmo.py

Receives pre-formatted human-readable steps (as JSON) from Claude
and pushes them to Testmo via REST API.

Input JSON format:
    {
        "name": "test_case_name",
        "description": "Optional description",
        "steps": [
            {
                "text1": "1. Navigate to page\n2. Enter '1770' in search field",
                "text3": "1. Verify 1 result returned\n2. Verify result ID equals '1770'"
            }
        ]
    }

Usage:
    python3 push_to_testmo.py steps.json \\
        --url https://xxx.testmo.net \\
        --token TOKEN \\
        --project-id ID \\
        [--folder-id FID]
"""
import json, sys, requests, argparse
from pathlib import Path


def get_cases_by_name(base_url, headers, project_id, name):
    """Return list of {id, folder_id} for all cases matching the given name."""
    matches = []
    page    = 1
    while True:
        r = requests.get(
            f"{base_url}/api/v1/projects/{project_id}/cases",
            headers=headers, params={"page": page, "per_page": 100}, timeout=30
        )
        r.raise_for_status()
        data = r.json()
        for case in data.get("result", []):
            if case["name"] == name:
                matches.append({"id": case["id"], "folder_id": case.get("folder_id")})
        if page >= data.get("last_page", 1):
            break
        page += 1
    return matches


def to_html(text):
    """Convert plain text (\\n line breaks) to Testmo HTML format."""
    if not text:
        return ""
    lines = [l for l in text.strip().split("\n") if l.strip()]
    return "<p>" + "<br>".join(lines) + "</p>"


def error_hint(code):
    return {
        401: "Token invalid or expired — regenerate from Testmo profile → API Tokens.",
        403: "Token lacks access to this project.",
        404: "Wrong project ID or Testmo URL.",
    }.get(code, "")


def main():
    p = argparse.ArgumentParser(description="Push formatted test steps to Testmo")
    p.add_argument("steps_json", help="JSON file with test case name and human-readable steps")
    p.add_argument("--url",        required=True)
    p.add_argument("--token",      required=True)
    p.add_argument("--project-id", required=True, type=int)
    p.add_argument("--folder-id",  type=int, default=None,
                   help="Only applied when CREATING a new case (ignored on updates)")
    p.add_argument("--tags", help="Comma-separated tags to add to the test case")
    p.add_argument("--template-id", type=int, default=None,
                   help="Template ID for the test case (e.g., 3 for Case (text))")
    args = p.parse_args()

    base_url = args.url.rstrip("/")
    pid      = args.project_id
    headers  = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
    }

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    data        = json.loads(Path(args.steps_json).read_text(encoding="utf-8"))
    name        = data["name"]
    description = data.get("description", "")
    steps       = [
        {"text1": to_html(s.get("text1", "")), "text3": to_html(s.get("text3", ""))}
        for s in data["steps"]
    ]

    print(f"Case  : {name}")
    print(f"Steps : {len(steps)}")

    # Find existing cases with this name
    print(f"\nSearching project {pid} for '{name}'...")
    try:
        matches = get_cases_by_name(base_url, headers, pid, name)
    except requests.HTTPError as e:
        print(f"Error: {e.response.status_code}. {error_hint(e.response.status_code)}")
        sys.exit(1)

    if matches:
        # Keep the first match; delete extras
        primary = matches[0]
        extras  = matches[1:]

        if extras:
            extra_ids = [c["id"] for c in extras]
            print(f"  Found {len(matches)} matches — deleting {len(extras)} duplicate(s): {extra_ids}")
            rd = requests.delete(f"{base_url}/api/v1/projects/{pid}/cases",
                                 headers=headers, json={"ids": extra_ids}, timeout=30)
            rd.raise_for_status()

        case_id = primary["id"]
        print(f"  Updating case (id={case_id}, folder={primary['folder_id']}) — keeping existing folder...")

        # PATCH bulk update: ids + custom_steps
        # ⚠️  No folder_id — avoids moving case to a different folder
        payload = {
            "ids":          [case_id],
            "custom_steps": steps,
        }
        if description:
            payload["custom_description"] = to_html(description)
        if tags:
            payload["tags"] = tags

        try:
            r = requests.patch(f"{base_url}/api/v1/projects/{pid}/cases",
                               headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            print(f"✅  Updated '{name}' (id={case_id})")
        except requests.HTTPError as e:
            print(f"Update error: {e.response.status_code}. {error_hint(e.response.status_code)}")
            print(e.response.text[:300])
            sys.exit(1)

    else:
        print(f"  Not found — creating new case...")
        payload = {"name": name, "custom_steps": steps}
        if description:
            payload["custom_description"] = to_html(description)
        if args.folder_id:
            payload["folder_id"] = args.folder_id
            print(f"  Placing in folder {args.folder_id}")
        if tags:
            payload["tags"] = tags
        if args.template_id:
            payload["template_id"] = args.template_id
            print(f"  Using template ID {args.template_id}")

        try:
            r = requests.post(f"{base_url}/api/v1/projects/{pid}/cases",
                              headers=headers, json={"cases": [payload]}, timeout=60)
            r.raise_for_status()
            resp   = r.json().get("result") or r.json().get("data") or [{}]
            new_id = resp[0].get("id", "?") if resp else "?"
            print(f"✅  Created '{name}' (id={new_id})")
        except requests.HTTPError as e:
            print(f"Create error: {e.response.status_code}. {error_hint(e.response.status_code)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
