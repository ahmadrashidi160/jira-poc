import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# API endpoint for search with JQL
url = f"{JIRA_BASE_URL}/rest/api/3/search"

# JQL to get all issues in project KAN
query = {
    'jql': 'project = KAN',
    'maxResults': 50,  # Can go up to 100; for full data you'll need pagination
    'fields': 'summary,key,assignee,status'
}

# Make the request
response = requests.get(
    url,
    params=query,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={"Accept": "application/json"}
)

# Process and print results
if response.status_code == 200:
    issues = response.json().get('issues', [])
    print(f"Found {len(issues)} issues in project KAN:\n")
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        assignee = issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else "Unassigned"
        print(f"{key}: {summary} [{status}] - {assignee}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
