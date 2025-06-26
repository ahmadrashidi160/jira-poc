import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load credentials
load_dotenv()
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# Set valid project options only
project = st.selectbox("Select Project", ["KAN", "SUP"])

# Action selector
action = st.radio("Action", ["View Issues", "Create Issue"])

# View Issues logic
if action == "View Issues":
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    query = {
        "jql": f"project = {project}",
        "maxResults": 10,
        "fields": "summary,key,assignee,status"
    }

    response = requests.get(
        url,
        params=query,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )

    if response.status_code == 200:
        issues = response.json()["issues"]
        st.write(f"### Showing issues for project `{project}`")
        for issue in issues:
            key = issue['key']
            summary = issue['fields']['summary']
            status = issue['fields']['status']['name']
            st.markdown(f"- **{key}**: {summary} `[Status: {status}]`")
    else:
        st.error("Failed to fetch issues.")

# Create Issue logic
elif action == "Create Issue":
    summary = st.text_input("Summary")
    description = st.text_area("Description")

    if st.button("Create"):
        url = f"{JIRA_BASE_URL}/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"text": description, "type": "text"}]
                    }]
                },
                "issuetype": {"name": "Task"}
            }
        }

        response = requests.post(
            url,
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=payload
        )

        if response.status_code == 201:
            st.success(f"Issue created: {response.json()['key']}")
        else:
            st.error(f"Failed to create issue: {response.status_code}")
