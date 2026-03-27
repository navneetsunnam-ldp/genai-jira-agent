import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

BASE_URL = "https://zemoso.atlassian.net"


def call_mcp(action, params=None):
    if params is None:
        params = {}

    if action == "get_sprints":
        return get_sprints()

    elif action == "get_issues_by_sprint":
        return get_issues_by_sprint(params.get("sprint_id"))

    elif action == "get_issues":
        return get_issues()

    return {"error": "Unknown action"}


def get_sprints():
    url = f"{BASE_URL}/rest/agile/1.0/board/294/sprint"

    return requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    ).json()


def get_issues_by_sprint(sprint_id):
    url = f"{BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"

    return requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    ).json()


def get_issues():
    url = f"{BASE_URL}/rest/api/3/search"

    return requests.get(
        url,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        params={"jql": "project=BC72", "expand": "changelog"}
    ).json()