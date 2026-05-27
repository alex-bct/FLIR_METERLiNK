#!/usr/bin/env python3
import json
import re
import sys
from html import unescape


def storage_html_to_text(html: str) -> str:
    s = html
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)<\s*li[^>]*>", "- ", s)
    s = re.sub(r"(?i)</\s*(p|div|li|tr|h1|h2|h3|h4|h5|h6|ul|ol|table)\s*>", "\n", s)
    s = re.sub(r"(?is)<pre[^>]*>(.*?)</pre>", lambda m: "\n```\n" + strip_tags(m.group(1)).strip() + "\n```\n", s)
    s = re.sub(r"(?is)<code[^>]*>(.*?)</code>", lambda m: "`" + strip_tags(m.group(1)).strip() + "`", s)
    s = strip_tags(s)
    s = unescape(s)
    s = re.sub(r"\r\n?", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


def strip_tags(s: str) -> str:
    return re.sub(r"(?is)<[^>]+>", "", s)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: storage_to_markdown.py <input_json> <output_md>", file=sys.stderr)
        return 2

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Untitled")
    version_num = data.get("version", {}).get("number", "unknown")
    space_name = data.get("space", {}).get("name", "unknown")
    html = data.get("body", {}).get("storage", {}).get("value", "")

    body = storage_html_to_text(html)
    output = (
        f"# {title}\n\n"
        f"- page_id: {data.get('id', 'unknown')}\n"
        f"- space: {space_name}\n"
        f"- version: {version_num}\n\n"
        f"{body}"
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
