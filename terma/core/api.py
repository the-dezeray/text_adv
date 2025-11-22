from typing import List
def get_community_stories() -> List[str]:
    """Fetch community stories from the backend API."""
    import requests

    url = "http://localhost:8001/community-stories"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            return result.get("stories", [])
        else:
            #self.console.print(f"Error: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        #self.console.print(f"Failed to fetch community stories: {e}")
        return []