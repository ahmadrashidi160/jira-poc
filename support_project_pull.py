import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# This is the Service Desk project key
PROJECT_KEY = "SUP"

# Jira search API endpoint with JQL
url = f"{JIRA_BASE_URL}/rest/api/3/search"
query = {
    'jql': f'project = {PROJECT_KEY}',
    'maxResults': 50,
    'fields': 'summary,key,status,assignee'
}

# Make the API call
response = requests.get(
    url,
    params=query,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={"Accept": "application/json"}
)

# Handle the response
if response.status_code == 200:
    issues = response.json().get('issues', [])
    print(f"Found {len(issues)} issues in project {PROJECT_KEY}:\n")
    for issue in issues:
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        assignee = issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else "Unassigned"
        print(f"{key}: {summary} [{status}] - {assignee}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
