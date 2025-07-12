def get_projects(client):
    """
    Get all projects from Jira API.
    
    Args:
        client (APIClient): An instance of the APIClient to make requests.
    
    Returns:
        list: A list of projects retrieved from the API.
    """
    projects = []
    startAt = 0
    max_results = 50
    while True:
        params = {
            "startAt": startAt,
            "maxResults": max_results,
            "expand": "description,lead,url"
        }
        
        response = client.get_request("Jira", "rest/api/3/project/search", params=params)
        
        if not response:
            raise Exception(f"Failed to fetch projects: {response}")
        
        data = response.json()
        projects.extend(data.get("values", []))
        
        if len(data) < max_results:
            break
        
        startAt += max_results
    return projects
