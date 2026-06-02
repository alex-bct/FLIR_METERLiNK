---
name: automation-runner
description: >
  Use this skill when the user wants to run Android smoke tests, check test results,
  or ask about the current state of the FLIR METERLiNK automation suite.
  This skill knows every available test case, suite, and how to interpret results.json.
  Trigger when the user says things like: "幫我跑測試", "run smoke test", "跑 oobe",
  "執行 mock-suite", "看測試結果", "上次跑的結果怎樣".
---

# FLIR METERLiNK — Automation Runner Skill

This skill gives you full control over the Android smoke test suite for the FLIR METERLiNK (SV95) project.
You do NOT need to know Python or ADB to use it — just tell the AI what you want in plain language.

---

## 1. 專案根目錄

All commands must be run from the project root:

```
/Users/alex/Documents/Project/FLIR_METERLiNK
```

When running any script, always `cd` to this directory first, or use it as the working directory.

---

## 2. 可用測試案例 (Available Test Cases)

### 單一案例 (Single Cases)

| 指令名稱 | 說明 | 需要實體裝置？ |
|:---------|:-----|:-------------|
| `oobe-allow` | 開啟 App → 同意定位權限 → 進入掃描頁 | ✅ 是 |
| `oobe-deny` | 開啟 App → 拒絕定位權限 → 驗證提示 | ✅ 是 |
| `search-no-device` | 搜尋頁面（沒有儀表）→ 驗證空狀態提示 | ✅ 是 |
| `cant-connect` | 點擊「Can't connect?」→ 驗證返回 | ✅ 是 |
| `mock-home-disconnected` | 首頁裝置卡片顯示「已斷線」狀態 | ❌ 不需要（用 Mock 資料）|
| `mock-device-detail-disconnected` | 裝置詳情頁斷線狀態 | ❌ 不需要 |
| `mock-gallery-empty` | Gallery 空狀態畫面 | ❌ 不需要 |
| `mock-add-device-default-name` | 新增裝置預設名稱流程 | ❌ 不需要 |
| `mock-delete-device-card` | 刪除裝置卡片流程 | ❌ 不需要 |

### 套件 (Suites — 一次跑多個)

| 套件名稱 | 包含案例 | 說明 |
|:---------|:---------|:-----|
| `oobe-suite` | oobe-allow, oobe-deny, search-no-device, cant-connect | 首次啟動完整流程 |
| `mock-suite` | mock-add-device-default-name, mock-home-disconnected, mock-device-detail-disconnected, mock-gallery-empty | 不需實體裝置的 Mock 測試 |

---

## 3. 執行測試的指令

### 跑單一案例
```bash
python3 scripts/flir_android_smoke.py --case <案例名稱>
```

**例子：**
```bash
python3 scripts/flir_android_smoke.py --case cant-connect
python3 scripts/flir_android_smoke.py --case oobe-allow
```

### 跑完整套件
```bash
python3 scripts/flir_android_smoke.py --case oobe-suite
```

### 跑 Mock 套件（不需要實體手機）
```bash
python3 scripts/flir_android_smoke.py --case mock-suite --mock-profile scripts/flir_android/mock_profile.json
```

### 指定特定手機（同時插多台時）
```bash
python3 scripts/flir_android_smoke.py --serial <裝置序號> --case oobe-suite
```

---

## 4. 測試結果在哪裡

每次跑完，結果會存在：

```
artifacts/android_smoke/
├── results.json        ← 所有案例的 PASS/FAIL 彙總
├── *.png               ← 各步驟截圖
└── *.xml               ← UI hierarchy dump（除錯用）
```

### 如何解讀 results.json

```json
{
  "results": [
    {
      "case_id": "SMK-07",
      "status": "PASS",
      "message": ""
    },
    {
      "case_id": "SMK-06",
      "status": "FAIL",
      "message": "Element 'Can't connect?' not found within 10s"
    }
  ]
}
```

- `status: "PASS"` → 測試通過 ✅
- `status: "FAIL"` → 測試失敗 ❌，`message` 說明原因

---

## 5. 常見問題排查

| 問題 | 原因 | 解法 |
|:-----|:-----|:-----|
| `adb: command not found` | ADB 未安裝或不在 PATH | 安裝 Android Platform Tools |
| `no devices/emulators found` | 手機未連接或未開啟 USB 偵錯 | 確認手機 → 開發者模式 → USB 偵錯 → 連接 USB |
| `INSTALL_FAILED_*` | App 未安裝 | 先在手機安裝 FLIR METERLiNK APK |
| Mock 案例失敗 | mock_profile.json 不存在 | 執行 `cp scripts/flir_android/mock_profile.example.json scripts/flir_android/mock_profile.json` |

---

## 6. AI 操作規則

當使用者說以下任何話，**主動幫他執行對應的 shell 指令**：

| 使用者說的 | AI 應執行 |
|:-----------|:---------|
| 「幫我跑 smoke test」/ 「跑全部測試」 | `python3 scripts/flir_android_smoke.py --case oobe-suite` |
| 「跑 mock」/ 「跑 mock 測試」 | `python3 scripts/flir_android_smoke.py --case mock-suite --mock-profile scripts/flir_android/mock_profile.json` |
| 「跑 cant-connect」(或任何單一案例名) | `python3 scripts/flir_android_smoke.py --case cant-connect` |
| 「看結果」/ 「上次結果」/ 「test result」 | 讀取 `artifacts/android_smoke/results.json` 並用中文摘要 PASS/FAIL |
| 「截圖」/ 「有沒有截圖」 | 列出 `artifacts/android_smoke/*.png` 並顯示最新截圖 |
| 「哪些 case 可以跑？」 | 列出上方第 2 節的所有案例表格 |

執行後，永遠用中文回報：
1. 執行了什麼指令
2. 哪幾個案例 PASS / FAIL
3. FAIL 的話，`message` 說了什麼
