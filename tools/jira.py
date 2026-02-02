import httpx
from tools.auth import BASE_URL, get_auth_header

JIRA_API = f"{BASE_URL}/rest/api/3"

# ------------------------
# Basic Issue Operations
# ------------------------

async def addCommentToJiraIssue(issue_key: str, comment: str) -> dict:
    url = f"{JIRA_API}/issue/{issue_key}/comment"
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"text": comment, "type": "text"}
                    ]
                }
            ]
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers={**get_auth_header(), "Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        return r.json()

async def addWorklogToJiraIssue(issue_key: str, time_spent_seconds: int = None, comment: str = None) -> dict:
    url = f"{JIRA_API}/issue/{issue_key}/worklog"
    payload = {}
    if time_spent_seconds:
        payload["timeSpentSeconds"] = time_spent_seconds
    if comment:
        payload["comment"] = {
            "type": "doc",
            "version": 1,
            "content": [{"type":"paragraph","content":[{"type":"text","text":comment}]}]
        }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers={**get_auth_header(), "Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        return r.json()

async def createJiraIssue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> dict:
    url = f"{JIRA_API}/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph","content":[{"type":"text","text":description}]}]
            },
            "issuetype": {"name": issue_type}
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers={**get_auth_header(), "Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        return r.json()

async def editJiraIssue(issue_key: str, fields: dict) -> dict:
    url = f"{JIRA_API}/issue/{issue_key}"
    payload = {"fields": fields}
    async with httpx.AsyncClient() as client:
        r = await client.put(url, headers={**get_auth_header(), "Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        return {"status": "success", "issue_key": issue_key}

async def getJiraIssue(issue_key: str) -> dict:
    url = f"{JIRA_API}/issue/{issue_key}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header())
        r.raise_for_status()
        return r.json()

async def getJiraIssueRemoteIssueLinks(issue_key: str) -> list:
    url = f"{JIRA_API}/issue/{issue_key}/remotelink"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header())
        r.raise_for_status()
        return r.json()

# -----------------------------------
# Metadata and Helper Endpoints
# -----------------------------------

async def getJiraIssueTypeMetaWithFields(project_key: str, issue_type_id: str) -> dict:
    url = f"{JIRA_API}/issue/createmeta"
    params = {
        "projectKeys": project_key,
        "issuetypeIds": issue_type_id,
        "expand": "projects.issuetypes.fields"
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header(), params=params)
        r.raise_for_status()
        return r.json()

async def getJiraProjectIssueTypesMetadata(project_key: str) -> list:
    url = f"{JIRA_API}/project/{project_key}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header())
        r.raise_for_status()
        return r.json().get("issueTypes", [])

async def getTransitionsForJiraIssue(issue_key: str) -> list:
    url = f"{JIRA_API}/issue/{issue_key}/transitions"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header())
        r.raise_for_status()
        return r.json().get("transitions", [])

async def getVisibleJiraProjects() -> list:
    # Uses the new /project/search endpoint
    url = f"{JIRA_API}/project/search"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header())
        r.raise_for_status()
        return r.json().get("values", [])

async def lookupJiraAccountId(query: str) -> list:
    url = f"{JIRA_API}/user/search"
    params = {"query": query}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=get_auth_header(), params=params)
        r.raise_for_status()
        return r.json()

async def transitionJiraIssue(issue_key: str, transition_id: str) -> dict:
    url = f"{JIRA_API}/issue/{issue_key}/transitions"
    payload = {"transition": {"id": transition_id}}
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers={**get_auth_header(), "Content-Type": "application/json"}, json=payload)
        r.raise_for_status()
        return {"status": "success", "issue_key": issue_key, "transition_id": transition_id}

# -------------------------------------
# Enhanced Search with new JQL API
# -------------------------------------

async def searchJiraIssuesUsingJql(
    jql: str,
    max_results: int = 50,
    next_page_token: str | None = None
) -> dict:
    """
    Search Jira using the new enhanced JQL endpoint.
    Handles pagination internally using nextPageToken.
    Returns:
        {"issues": [...], "nextPageToken": "...", "isLast": ...}
    """
    url = f"{JIRA_API}/search/jql"
    headers = {**get_auth_header(), "Accept": "application/json"}
    params = {"jql": jql, "maxResults": max_results}

    # Add token if available
    if next_page_token:
        params["nextPageToken"] = next_page_token

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

async def searchAllJiraIssues(
    jql: str,
    max_results: int = 50
) -> list:
    """
    Loop through pages using nextPageToken to collect all issues.
    """
    results = []
    token = None

    while True:
        page = await searchJiraIssuesUsingJql(jql, max_results, token)
        results.extend(page.get("issues", []))

        # Stop if no more pages
        if page.get("isLast"):
            break

        token = page.get("nextPageToken")

    return results
