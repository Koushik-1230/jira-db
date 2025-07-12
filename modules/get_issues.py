""" Get all issue from Jira API Paginated
"""
from .get_projects import get_projects

def get_issues(client):
    """
    Get issues from Jira API with pagination.
    
    Args:
        request_to (str): The service to make the request to (e.g., "jira").
        endpoint (str): The API endpoint to fetch issues from.
    
    Returns:
        list: A list of issues retrieved from the API.
    """
    issues = []
    projects = get_projects(client)
    if not projects:
        raise Exception("No projects found to fetch issues from.")
    for project in projects:
        project_key = project.get("key")
        if not project_key:
            continue
        client.logger.info(f"Fetching issues for project: {project_key}") 
        nextPageToken = None
        max_results = 10

        while True:
            params = {
                "maxResults": max_results,
                "fields": "summary,description,status,assignee,reporter,created,updated,project",
                "jql": f'project= {project_key} order by created DESC'
            }
            if nextPageToken:
                params["nextPageToken"] = nextPageToken
            
            response = client.get_request("Jira", "rest/api/3/search/jql", params=params)
            
            if not response:
                raise Exception(f"Failed to fetch issues: {response}")
            
            data = response.json()
            issues.extend(data.get("issues", []))
            nextPageToken = data.get("nextPageToken")
            if not nextPageToken:
                break

    return issues
    