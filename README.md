# FLIR METERLiNK Automation & Project Repository

Welcome to the **FLIR METERLiNK (SV95)** project repository. This codebase aggregates product specifications, vibration severity standards (ISO 10816), and Android UI smoke test automation scripts.

Additionally, this repository provides structured **AI agent skills** inside the `skills/` directory to help AI developers and agentic workflows operate seamlessly on tasks related to Jira syncing, Testmo publishing, Confluence integration, and FLIR METERLiNK specifications.

---

## 📂 Project Structure

```text
├── README.md                           # Main project documentation
├── Meterlink.md                        # SV95 Full Spec & Project Panorama
├── android_smoke_cases_no_device.md    # Android smoke testing cases checklist
├── DM285_CM275 Range Data.xlsx         # Range data specifications
├── FLIR_QA_TCs_METERLiNK.xlsx          # QA full test cases
├── Meterlink_Protocol_Definition.pdf   # Official BLE protocol spec (v4.2.14)
├── Meterlink_Visual.svg                # Protocol state diagrams
├── scripts/
│   ├── flir_android_smoke.py           # CLI entry point for Android smoke tests
│   ├── flir_android/                   # UI test automation package
│   ├── push_to_testmo.py               # Push test scripts to Testmo API
│   └── qa_daily_report.py              # QA reporting helper script
└── skills/
    ├── flir-meterlink-expert/          # FLIR METERLiNK SV95 spec skill (AI agent ready)
    ├── vibration-iso-expert/           # Machine vibration ISO 10816 rule engine skill
    ├── jira-ops/                       # Jira ticket read/write skill
    ├── testmo-sync/                    # Pytest-to-Testmo syncing skill
    └── atlassian-confluence-fetch/     # Confluence API documentation fetching skill
```

---

## 🧠 AI Agent Skills Ready

This project is fully equipped with AI-agent skills located under `/skills`. These are specialized Markdown blueprints with structured playbooks that empower agentic tools (like Gemini/Codex) to automate complex tasks.

1.  **[FLIR METERLiNK Expert](skills/flir-meterlink-expert/SKILL.md)**: BLE connection sequences, RTC clock-syncs, unit-switching logic, alarm popup formats, and the smoke suite checklist.
2.  **[Vibration ISO Expert](skills/vibration-iso-expert/SKILL.md)**: Validates vibration levels on SV95. Comes with a lookup engine:
    ```bash
    python3 skills/vibration-iso-expert/scripts/iso_10816_lookup.py large rigid 5.2 mm/s
    ```
3.  **[Testmo Sync Playbook](skills/testmo-sync/SKILL.md)**: Automatically parses Python pytest cases using AST and registers them via REST API.
4.  **[Jira Operations](skills/jira-ops/SKILL.md)**: Connects to Jira Cloud, transitions workflows, updates descriptions, and adds comments safely.
5.  **[Confluence Fetcher](skills/atlassian-confluence-fetch/SKILL.md)**: Imports specifications and pages directly into local workspace markdown format.

---

## 📱 Android Smoke Testing

We have built a non-device smoke testing suite for quick OOBE and settings page validations using standard `adb` interactions.

### Prerequisites
1.  Connect your Android phone with USB debugging enabled.
2.  Install the FLIR METERLiNK beta package (`com.flir.METERLiNKAPP.beta`).
3.  Make sure `adb` is available in your shell `PATH`.

### Running Tests
Run the entire mock suite:
```bash
cp scripts/flir_android/mock_profile.example.json scripts/flir_android/mock_profile.json
python3 scripts/flir_android_smoke.py --case mock-suite --mock-profile scripts/flir_android/mock_profile.json
```

Run specific case:
```bash
python3 scripts/flir_android_smoke.py --case cant-connect
```

All test outcomes, screenshots, and XML window hierarchies are stored inside `artifacts/android_smoke/`.

---
*Developed with Advanced Agentic Coding by Antigravity.*
