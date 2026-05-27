import json
import requests
import os
import time

# Sourcing credentials from .env
env = {}
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v

site = env['ATLASSIAN_SITE']
email = env['ATLASSIAN_EMAIL']
token = env['ATLASSIAN_TOKEN']
auth = (email, token)
board_id = 223
base_url = f"https://{site}/rest/agile/1.0/board/{board_id}/issue"

all_issues = []
start_at = 0
max_results = 100

print(f"Starting fetch for all issues from board {board_id}...")

while True:
    url = f"{base_url}?startAt={start_at}&maxResults={max_results}&fields=summary,status,issuetype,updated,description"
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        print(f"Error fetching at {start_at}: {response.status_code}")
        break
    
    data = response.json()
    issues = data.get('issues', [])
    all_issues.extend(issues)
    
    print(f"Fetched {len(all_issues)} / {data.get('total', 'unknown')}...")
    
    if len(issues) < max_results:
        break
    start_at += max_results
    time.sleep(0.5) # Avoid rate limiting

with open('artifacts/jira_fm_all_tickets.json', 'w') as f:
    json.dump(all_issues, f)

print(f"Successfully saved {len(all_issues)} tickets.")
