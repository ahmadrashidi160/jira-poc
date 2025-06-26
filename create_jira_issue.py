import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json

# Load .env variables
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# Endpoint to create an issue
url = f"{JIRA_BASE_URL}/rest/api/3/issue"

# Payload: adjust fields as needed
payload = {
    "fields": {
        "project": {
            "key": "KAN"  # Change as needed
        },
        "summary": "Test issue from API",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "This issue was created via Python using Jira REST API.",
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Task"  # Can be Bug, Story, Incident, etc.
        }
    }
}

# Send POST request to create issue
response = requests.post(
    url,
    data=json.dumps(payload),
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
)

# Handle response
if response.status_code == 201:
    issue_key = response.json()["key"]
    print(f"Issue created successfully: {issue_key}")
else:
    print(f"Failed to create issue. Status Code: {response.status_code}")
    print(response.text)
