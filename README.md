# FLIR METERLiNK - QA & Automation Workspace

這是一個專為 FLIR METERLiNK (特別是 SV95 型號) 打造的測試與開發資源庫。
旨在透過自動化腳本、標準化測試案例與 AI 技術知識，提升團隊的測試效率與對齊業務邏輯。

## 📂 專案結構指南

### 1. 自動化測試 (Automation Scripts)
*   **目錄**: `/scripts/flir_android/`
*   **用途**: 基於 ADB 與 UI Automator 的 Android Smoke Test 框架。
*   **特點**: 
    *   包含穩定的 Mock 測試腳本 (例如自動連點進入 Debug 模式、防動畫干擾的重啟機制)。
    *   **執行方式**: `python3 scripts/flir_android_smoke.py --case mock-suite`

### 2. 測試案例庫 (Test Cases)
*   **檔案**: `SV95_QA_Style_Full_TCs_Final_Clean.csv`
*   **用途**: 涵蓋 60+ 條 SV95 的功能測試案例，包含連線、UI 防呆 (Danger > Alert)、密碼限制 (6-8碼) 等。
*   **如何使用**: 可以直接複製並貼上到 Google Sheets 或 TestRail 中進行管理。

### 3. 技術知識庫 (Documentation)
*   **檔案**: `Meterlink.md`
    *   專案唯一的 Source of Truth，包含 Jira Ticket (FM-13xx 系列) 與核心功能的對應。
*   **檔案**: `SV95_CONCEPTS.md`
    *   **推薦新進同事閱讀**！用最直白的比喻（心跳頻率 vs 摸脈搏時間）解釋了 BLE / Wi-Fi / MQTT 的分工，以及各項參數的 UI 限制。

### 4. Gemini CLI 專家技能 (AI Skills)
*   **目錄**: `/skills/`
*   **用途**: 這是 AI 專家的「知識腦核」。我們將專案特有的業務規則、通訊規範與 ISO 標準封裝成可重複使用的技能。
*   **組成**:
    *   `mqtt-protocol-skill/`: 包含 MQTT 驗證邏輯與密碼規範。
    *   `vibration-iso-expert/`: 提供 ISO 10816 振動等級查詢功能。
*   **如何使用與開發**:
    *   **安裝**: 執行 `gemini skills install mqtt-protocol-skill.skill --scope workspace`。
    *   **更新**: 如果規範有變，直接修改 `skills/` 內的 MD 檔並重新打包，即可讓全團隊的 AI 助手同步更新知識。

---
*Maintained by QA/Dev Team*
