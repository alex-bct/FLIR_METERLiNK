# FLIR METERLiNK - QA & Automation Workspace

這是一個專為 FLIR METERLiNK (特別是 SV95 型號) 打造的測試與開發資源庫。
旨在透過自動化腳本、標準化測試案例與 AI 技術知識，提升團隊的測試效率與對齊業務邏輯。

## 📂 專案結構指南

## 🚀 快速開始 (Quick Start)

因為本專案的設計訴求為簡單、無腦使用，您可以依照以下幾個基本步驟快速執行：

1. **取得程式碼**：
   ```bash
   git clone <你的 repo 網址>
   cd FLIR_METERLiNK
   ```
2. **安裝基本套件**：
   本專案主要使用 Python 開發，執行前請安裝必要的依賴套件（例如 `requests`）：
   ```bash
   pip install requests
   # 或者是如果您有產生 requirements.txt
   # pip install -r requirements.txt
   ```
3. **設定環境變數**：
   複製環境變數範本並填入對應的 Token 與資訊：
   ```bash
   cp .env.example .env
   ```
   *(請打開 `.env` 檔案並填入您的 Atlassian/Jira 資訊)*

4. **執行腳本**：
   - 抓取 Jira Tickets: `python fetch_all_tickets.py`
   - Android 自動化測試: `python3 scripts/flir_android_smoke.py --case mock-suite`

### 1. 自動化測試 (Automation Scripts)
*   **目錄**: `/scripts/flir_android/`
*   **用途**: 基於 ADB 與 UI Automator 的 Android Smoke Test 框架。
*   **特點**: 
    *   包含穩定的 Mock 測試腳本 (例如自動連點進入 Debug 模式、防動畫干擾的重啟機制)。
    *   **執行方式**: `python3 scripts/flir_android_smoke.py --case mock-suite`

### 2. 測試案例庫 (Test Cases)
*   **檔案**: `SV95_QA_Style_Full_TCs.md`
*   **用途**: 涵蓋 60+ 條 SV95 的功能測試案例，包含連線、UI 防呆 (Danger > Alert)、密碼限制 (6-8碼) 等。
*   **優勢**: 使用 Markdown 表格格式，在 GitHub 上具備完美的預覽效果，且非常適合 Git 版控（Diff 追蹤）。
*   **如何使用**: 可以直接在 GitHub 上預覽，或是複製貼上到 TestRail / Google Sheets 中進行管理。

### 3. 技術知識庫 (Documentation)
*   **檔案**: `Meterlink.md`
    *   專案唯一的 Source of Truth，包含 Jira Ticket (FM-13xx 系列) 與核心功能的對應。
*   **檔案**: `SV95_CONCEPTS.md`
    *   **推薦新進同事閱讀**！用最直白的比喻（心跳頻率 vs 摸脈搏時間）解釋了 BLE / Wi-Fi / MQTT 的分工，以及各項參數的 UI 限制。

### 4. Gemini CLI 專家技能 (AI Skills)
*   **目錄**: `/skills/`
*   **用途**: 這是 AI 專家的「知識腦核」。我們將專案特有的業務規則、通訊規範與 ISO 標準封裝成可重複使用的技能。
*   **組成 (目前包含 7 種核心技能)**:
    1. `atlassian-confluence-fetch/`: 用於從 Confluence 自動獲取產品文件與需求規格。
    2. `automation-runner/`: 輔助執行自動化測試流程與相關任務的腳本技能。
    3. `flir-meterlink-expert/`: 內建 FLIR METERLiNK 產品的核心業務邏輯、限制條件與知識庫。
    4. `jira-ops/`: 提供與 Jira 進行自動化互動的能力（例如查詢、更新 Tickets）。
    5. `mqtt-protocol-skill/`: 包含專案專屬的 MQTT 驗證邏輯與連線/密碼規範。
    6. `testmo-sync/`: 協助將測試案例或自動化測試結果同步至 Testmo 管理平台。
    7. `vibration-iso-expert/`: 提供 ISO 10816 振動等級標準與判定門檻的查詢功能。
*   **如何使用與更新技能**:
    *   **首次安裝**: 進入各個 skill 資料夾，執行 `gemini skills install <skill_name>.skill --scope workspace`。
    *   **如何取得最新更新 (一般使用者)**: 若有其他人更新了技能，您只需執行 `git pull` 拉取最新程式碼，並再次執行上述 `install` 指令覆蓋即可。
    *   **如何修改技能 (開發者)**: 若有業務邏輯或規範變更，請直接修改該 skill 目錄內的設定檔（如 MD/指令檔），再透過 git push 分享給團隊。

---
*Maintained by QA/Dev Team*
