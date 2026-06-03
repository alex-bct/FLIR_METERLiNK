# FLIR METERLiNK - SV95 專案全景知識庫

本文件彙整自最新規格頁面 (ID: 4020273173)，提供 SV95 開發、測試與連線邏輯的完整參考。

## 1. 核心功能與 Jira Ticket 映射
| 功能模組 | 說明 | 關鍵 Jira Ticket |
| :--- | :--- | :--- |
| **協定更新** | METERLiNK Protocol V4.2.15 | FM-1304 |
| **搜尋與連線** | 需移除 DFU 檢查以確保 SV95 可連線 | FM-1305 |
| **首頁卡片** | 顯示 OA (X/Y/Z) 與 溫度，含顏色警示 | FM-1306 |
| **裝置詳情** | 移除 Report 按鈕，新增趨勢圖表卡片 | FM-1307, FM-1308 |
| **圖表互動** | 支持數據過濾、雙 Y 軸、全螢幕 Marker | FM-1309, 1310, 1311 |
| **警報設定** | ISO 10816 選項 (Large/Medium/Small) | FM-1313 |
| **警報通知** | 數值超過門檻時顯示彈窗通知 | FM-1342 |
| **檔案管理** | SV95 不支援 Gallery，僅支援 Recording List | FM-1315, FM-1316 |
| **更多頁面** | 單位切換 (OA/Temp)、Wi-Fi/MQTT/Schedule | FM-1317, 1318, 1319 |
| **連線套用** | 從現有 SV95 裝置套用 Wi-Fi/MQTT 設定 | FM-1335, FM-1336 |
| **系統更新** | API Level 36, CVE Fix, Sign Key | FM-1301, 1337, 1338 |
| **介面優化** | 支援 Dark/Light Mode, Tablet | FM-1339, 1340 |

## 2. BLE 連線與資料同步邏輯
### 初始化順序 (Connection Sequence)
當 App 與 SV95 建立連線後，必須依序執行以下指令：
1.  **Set RTC (時鐘同步)**: 確保裝置紀錄正確的時間戳。 (FM-1320)
2.  **Get Info**: 依序獲取 Wi-Fi, MQTT 與 Schedule 資訊。 (FM-1321, 1323)
3.  **自動初始化 (Auto-Init)**:
    *   若 `Get Schedule Info` 回傳為空（預設 1970 年），App 必須自動呼叫 `Set Schedule Settings`。
    *   **預設值**: 開始於連線當天 00:00:00，結束於 3 年後，週一至週日全開，Sampling 2s，Interval 2 mins。

### More 頁面即時更新 (FM-1341)
*   每當進入 **More** 頁面時，App 必須主動發送 BLE 指令（Get Wi-Fi, MQTT, Schedule info）以獲取裝置最新狀態並更新 UI。

## 3. 單位切換連動邏輯 (Unit Switching)
在 More 頁面切換單位時，App 需處理以下連動動作：
*   **OA 單位 (mm/s ↔ inch/s)**:
    *   首頁卡片與詳情頁圖表即時重繪。
    *   警報門檻值按比例自動轉換。
*   **溫度單位 (°C ↔ °F)**:
    *   首頁卡片與詳情頁圖表即時重繪。
    *   **重要**: 根據 App 慣例，切換溫度單位會**清空 (Clear)** 當前的溫度警報設定。 (FM-1318)

## 4. 警報通知 (Notification - FM-1342)
當數值超過 Alert/Danger 門檻時，彈窗文案格式如下：
*   `%Device_name% meter measurement %value% is higher than [alert|danger] value %alarm_settings%`

## 5. 系統環境需求
*   **Target SDK**: Google API Level 36 (FM-1301)。
*   **外觀模式**: 完整支援系統 Dark Mode 與 Light Mode 切換 (FM-1339)。
*   **裝置支援**: 支援 Tablet 佈局（無須 UI 優化，但需相容 Dark Mode）(FM-1340)。

---
*Last Updated: 2026-05-06 by Gemini CLI (Ref: 4020273173, Version: 29)*
