#!/usr/bin/env python3
import json
import os
import datetime
from pathlib import Path

def generate_report():
    results_file = Path("artifacts/android_smoke/results.json")
    report_file = Path("artifacts/android_smoke/report.html")

    if not results_file.exists():
        print(f"Error: {results_file} not found. Please run the tests first.")
        return

    try:
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error reading results.json: {e}")
        return

    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = total - passed
    pass_rate = int((passed / total * 100) if total > 0 else 0)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cards_html = ""
    for r in results:
        status = r.get("status", "UNKNOWN")
        case_id = r.get("case_id", "Unknown ID")
        detail = r.get("detail", "")
        
        status_class = "status-pass" if status == "PASS" else "status-fail"
        icon = "✅" if status == "PASS" else "❌"
        
        # Check for screenshots related to this case if failed (rough match)
        screenshot_html = ""
        if status != "PASS":
            screenshot_html = f'<div class="screenshot-hint">📸 截圖已保留在資料夾中</div>'

        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="case-id">{case_id}</span>
                <span class="status-badge {status_class}">{icon} {status}</span>
            </div>
            <div class="card-body">
                <p>{detail}</p>
                {screenshot_html}
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FLIR METERLiNK Automation Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f172a;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --flir-green: #10b981;
            --flir-red: #ef4444;
            --accent: #3b82f6;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-primary);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 50px;
            animation: fadeInDown 0.8s ease-out;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(to right, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .meta-info {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
            animation: fadeIn 1s ease-out;
        }}

        .stat-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 10px 0;
        }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .value-pass {{ color: var(--flir-green); }}
        .value-fail {{ color: var(--flir-red); }}
        
        .results-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            animation: slideUp 0.8s ease-out;
        }}

        .card {{
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .card:hover {{
            background: rgba(45, 55, 72, 0.8);
            border-color: rgba(255, 255, 255, 0.2);
            transform: scale(1.01);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .case-id {{
            font-weight: 600;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
        }}

        .status-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .status-pass {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--flir-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .status-fail {{
            background: rgba(239, 68, 68, 0.15);
            color: var(--flir-red);
            border: 1px solid rgba(239, 68, 68, 0.3);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
        }}

        .card-body p {{
            margin: 0;
            color: #cbd5e1;
            line-height: 1.5;
            font-size: 0.95rem;
        }}
        
        .screenshot-hint {{
            margin-top: 12px;
            font-size: 0.85rem;
            color: #fca5a5;
            background: rgba(239, 68, 68, 0.1);
            padding: 8px 12px;
            border-radius: 6px;
            display: inline-block;
        }}

        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>FLIR METERLiNK Automation Dashboard</h1>
            <div class="meta-info">Report generated on {timestamp} • Environment: Android Smoke Test</div>
        </header>

        <div class="dashboard">
            <div class="stat-card">
                <div class="stat-label">Total Cases</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pass Rate</div>
                <div class="stat-value {'value-pass' if pass_rate == 100 else 'value-fail'}">{pass_rate}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Passed</div>
                <div class="stat-value value-pass">{passed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Failed</div>
                <div class="stat-value value-fail">{failed}</div>
            </div>
        </div>

        <div class="results-grid">
            {cards_html}
        </div>
    </div>
</body>
</html>"""

    report_file.write_text(html_content, encoding="utf-8")
    print(f"✅ Premium HTML report generated successfully at: {report_file}")

if __name__ == "__main__":
    generate_report()
