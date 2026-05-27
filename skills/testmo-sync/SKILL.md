---
name: testmo-sync
description: >
  Use this skill when the user wants to sync Python automation scripts to Testmo test case management.
  Trigger whenever the user mentions: uploading test steps to Testmo, syncing test scripts with Testmo,
  populating Testmo test cases from Python automation, parsing test files to create or update Testmo
  cases, or filling Testmo with steps from automation code. Also trigger for phrases like
  "把測試腳本同步到 Testmo", "把步驟填到 Testmo", "幫我把 pytest 上傳到 Testmo",
  "把 test case 步驟填入 Testmo", even when test case name is mentioned alongside Testmo.
---

# Testmo Sync Skill

Reads Python test functions (either `test_*` for pytest or `run` for local runner), interprets each code statement into human-readable English, then creates or updates test cases in Testmo via REST API.

The push script lives at: `scripts/push_to_testmo.py`
Default configuration is in: `skills/testmo-sync/.testmo_config.json`

---

## 1 — Collect inputs (ask if missing)

| Input | Example |
|---|---|
| Test file path | `scripts/flir_android/cases/mock_add_device_default_name.py` |
| Function name | `run` or `test_xxx` |
| Testmo URL | `https://bct-tpe.testmo.net` (from config) |
| API Token | (from config) |
| Project ID | `10` (numeric, from project URL) |
| Folder ID | optional, only for new cases |

---

## 2 — Parse the test function

Run this bash snippet to extract raw statements:

```bash
python3 - << 'PYEOF'
import ast
from pathlib import Path

file   = "<FILE_PATH>"
target = "<FUNCTION_NAME>"   # e.g., "run" or "test_xxx"

source = Path(file).read_text(encoding="utf-8")
tree   = ast.parse(source)

for node in ast.walk(tree):
    if not isinstance(node, ast.FunctionDef):
        continue
    # Match specific target or default patterns
    if target:
        if node.name != target: continue
    else:
        if not (node.name.startswith("test_") or node.name == "run"):
            continue

    print(f"\n=== {node.name} ===")
    docstring = ast.get_docstring(node)
    if docstring:
        print(f"[docstring] {docstring}")
    for stmt in node.body:
        if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)):
            continue  # skip docstring node
        kind = "ASSERT" if isinstance(stmt, ast.Assert) else "ACTION"
        print(f"  [{kind}] {ast.unparse(stmt)}")
PYEOF
```

---

## 3 — Interpret each statement into human-readable English

For every `[ACTION]` or `[ASSERT]` statement, write a natural English sentence.

### ACTION interpretation patterns

| Code pattern | English |
|---|---|
| `var = 'value'` | Set `var` to `'value'` |
| `xxx.get("url")` / `.navigate("url")` | Navigate to [page name or URL] |
| `.click_xxx()` | Click [xxx description] |
| `.input_xxx(value)` / `.send_keys(value)` | Enter `'value'` in [xxx] field |
| `.get_xxx()` / `.get_whole_table_contents(label='X')` | Retrieve [X] column contents |
| `.screenshot("name")` | Capture a screenshot named "name" |
| `.ensure_mock_device_added(profile)` | Ensure the mock device is correctly added and detected |
| `runner.record(CASE_ID, "PASS", ...)` | Record the test result as PASS with the given details |
| Method chain (a.b().c().d()) | Describe the whole chain as one sentence |

### ASSERT interpretation patterns

| Code pattern | English |
|---|---|
| `assert x == y` | Verify [x] equals [y] |
| `assert len(x) == n` | Verify [x] has exactly n result(s) |
| `assert x > 0` | Verify [x] is greater than 0 |
| `assert x in y` | Verify [x] is found in [y] |
| `assert x is True/False` | Verify [x] is True / False |
| `assert x.is_displayed()` | Verify [x] is visible on the page |

Use **English only**. Be concise and descriptive — no code syntax in the output.

---

## 4 — Group into Testmo steps

One Testmo "step" = a block of actions + the assertions that follow them immediately.

**Grouping algorithm:**
1. Collect consecutive ACTION statements → these go into `text1`
2. When you reach ASSERT statement(s) with no ACTION in between → they all go into `text3` of the same step
3. Start a new step when an ACTION appears after assertion(s)

**Formatting rules:**

`text1` — what to do:
- Single action → plain sentence (no number)
- Multiple actions → `1. sentence\n2. sentence\n3. sentence`

`text3` — expected result:
- Single assertion → plain sentence (no number)
- Multiple consecutive assertions → `1. sentence\n2. sentence`

---

## 5 — Write and push the JSON payload

Save the steps to `/tmp/testmo_steps.json`:

```json
{
  "name": "test_search_for_id",
  "description": "Optional docstring here",
  "steps": [
    {
      "text1": "1. Set the search keyword to '1770'\n2. ...",
      "text3": "1. Verify there is exactly 1 result\n2. ..."
    }
  ]
}
```

Then run:

```bash
python3 scripts/push_to_testmo.py \
  /tmp/testmo_steps.json \
  --url <TESTMO_URL> \
  --token <TOKEN> \
  --project-id <PROJECT_ID> \
  [--folder-id <FOLDER_ID>]
```

---

## 6 — Sync rules

| Situation | Action |
|---|---|
| Case with same name exists in project | **Update** steps only (never change folder) |
| Case not found | **Create** new (apply folder_id if given) |
| Never | Delete cases |
