import json
import os
import subprocess
from datetime import datetime, timedelta

def notify(title, message):
    # 彈出 Mac 系統通知
    subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
    # 同時在終端機打印
    print(f"\n[{title}] {message}\n")

def generate_report():
    # 1. 執行最新的抓取 (確保數據是最新的)
    # 這裡假設環境變數已在 .env 中，我們直接讀取並執行
    os.system("export $(grep -v '^#' .env | xargs) && curl -fsS -u \"${ATLASSIAN_EMAIL}:${ATLASSIAN_TOKEN}\" \"https://${ATLASSIAN_SITE}/rest/agile/1.0/board/223/issue?maxResults=100\" -o artifacts/jira_fm_board_all.json > /dev/null 2>&1")

    try:
        with open('artifacts/jira_fm_board_all.json', 'r') as f:
            issues = json.load(f).get('issues', [])
    except:
        return "資料抓取失敗，請檢查網路或 Token。"

    # 邏輯：找狀態為 Done 或 Code Reviewing 的 (通常是開發完成待 QA)
    to_verify = [i for i in issues if i['fields']['status']['name'] in ['Done', 'Code Reviewing']]
    
    if not to_verify:
        return "今日暫無待驗證項目。"

    msg = f"今日有 {len(to_verify)} 則 Ticket 待驗證：\n"
    for i in to_verify[:5]: # 只列前五個，避免通知過長
        msg += f"- {i['key']}: {i['fields']['summary']}\n"
    
    # 寫入本地檔案供隨時查看
    with open('TODAY_QA_TASKS.md', 'w') as f:
        f.write(f"# QA Daily Tasks ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        f.write("\n".join([f"- [{i['key']}](https://dt360.atlassian.net/browse/{i['key']}): {i['fields']['summary']}" for i in to_verify]))

    return f"發現 {len(to_verify)} 則待驗證項目，詳情已更新至 TODAY_QA_TASKS.md"

if __name__ == "__main__":
    content = generate_report()
    notify("METERLiNK QA 通報", content)
