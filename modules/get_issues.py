""" Get all issue from Jira API Paginated
"""

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
    start_at = 0
    max_results = 50  # Adjust as needed

    while True:
        params = {
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "summary,description,status",
            "jql": "ORDER BY created DESC"
        }
        
        response = client.get_request("Jira", "rest/api/2/issue", params=params)
        
        if not response:
            raise Exception(f"Failed to fetch issues: {response}")
        
        data = response.json()
        issues.extend(data.get("issues", []))
        
        if len(data.get("issues", [])) < max_results:
            break
        
        start_at += max_results

    return issues
    