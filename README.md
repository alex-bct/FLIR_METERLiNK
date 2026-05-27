# FLIR METERLiNK - AI Agent Skills Repository

Welcome to the **FLIR METERLiNK** AI Agent Skills Repository. This repository aggregates structured, production-ready AI skills and playbooks designed to empower agentic workflows (such as Gemini, Codex, or other LLM-based coding assistants) to operate autonomously, safely, and efficiently.

---

## 📂 Repository Structure

This repository focuses exclusively on modular AI skill blueprints:

```text
├── README.md                           # Main repository documentation
└── skills/
    ├── flir-meterlink-expert/          # FLIR METERLiNK SV95 spec skill (AI agent ready)
    ├── vibration-iso-expert/           # Machine vibration ISO 10816 rule engine skill
    ├── jira-ops/                       # Jira ticket read/write skill
    ├── testmo-sync/                    # Pytest-to-Testmo syncing skill
    └── atlassian-confluence-fetch/     # Confluence API documentation fetching skill
```

---

## 🧠 AI Agent Skills Overview

Each skill directory under `skills/` contains a specialized `SKILL.md` file equipped with a YAML frontmatter definition. These serve as direct execution playbooks:

### 1. 📱 [FLIR METERLiNK Expert](skills/flir-meterlink-expert/SKILL.md)
*   **Purpose**: Encapsulates product specifications for the SV95 BLE device integration.
*   **Key Features**:
    *   **BLE Connect Sequence**: Clock synchronization (RTC) and auto-initialization rules.
    *   **Unit Conversion Rules**: Metric (`mm/s`, `°C`) to imperial (`inch/s`, `°F`) translation behaviors, including temperature alarm reset rules.
    *   **Alarm Notification Format**: String templates for system-level alarm warnings.
    *   **Android Smoke Cases**: Checklists for `SMK-01` through `SMK-15` without requiring physical Bluetooth hardware.

### 2. 🛡️ [Vibration ISO Expert](skills/vibration-iso-expert/SKILL.md)
*   **Purpose**: Evaluates machine vibration severity based on the ISO 10816 standard.
*   **Key Features**:
    *   Vibration threshold classifications (Rigid vs. Flexible foundations).
    *   Machine size categories (Large, Medium, Small).
    *   Includes a Python lookup automation script:
        ```bash
        python3 skills/vibration-iso-expert/scripts/iso_10816_lookup.py large rigid 5.2 mm/s
        ```

### 3. 🧪 [Testmo Sync Playbook](skills/testmo-sync/SKILL.md)
*   **Purpose**: Maps AST (Abstract Syntax Trees) from Python automation test cases to human-readable step definitions and pushes them to Testmo API.
*   **Key Features**:
    *   Automated token and configuration parsing.
    *   Action/Assertion matching rules.
    *   Payload generation schema and workflow.

### 4. 🎫 [Jira Operations](skills/jira-ops/SKILL.md)
*   **Purpose**: Automates Jira issue CRUD operations while adhering to safety-first boundaries.
*   **Key Features**:
    *   Idempotent reads and transitions.
    *   Preservation of description templates.
    *   discoverable workflow field matching.

### 5. 📖 [Confluence Fetcher](skills/atlassian-confluence-fetch/SKILL.md)
*   **Purpose**: Fetches REST storage representations from Confluence and syncs them to clean Markdown files in local workspaces.

---
*Developed with Advanced Agentic Coding by Antigravity.*
