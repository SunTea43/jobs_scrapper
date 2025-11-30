import requests
import json
from urllib.parse import urlencode

class LinkedInJobsClient:
    def __init__(self, access_token: str):
        self.base_url = "https://api.linkedin.com/v2/"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def search_jobs(self, query: str, location: str = None, limit: int = 25) -> dict:
        """
        Search job vacancies by a position name.
        Note: Requires authorized access to LinkedIn Jobs API.
        """

        params = {
            "q": "search",
            "keywords": query,
            "count": limit
        }

        if location:
            params["location"] = location

        url = f"{self.base_url}jobSearch?{urlencode(params)}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"LinkedIn API error: {response.status_code} - {response.text}")

        data = response.json()

        # Normalize data for cleaner JSON output
        results = []
        for item in data.get("elements", []):
            job = {
                "title": item.get("title"),
                "companyName": item.get("companyName"),
                "location": item.get("formattedLocation"),
                "listedAt": item.get("listedAt"),
                "jobPostingUrl": item.get("jobPostingUrl"),
                "jobId": item.get("jobPostingId")
            }
            results.append(job)

        return {
            "query": query,
            "count": len(results),
            "results": results
        }


# --------------------
# Example usage
# --------------------
if __name__ == "__main__":
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

    linkedin = LinkedInJobsClient(access_token=ACCESS_TOKEN)

    try:
        data = linkedin.search_jobs(
            query="Designer",
            location="Colombia",
            limit=20
        )

        print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error: {e}")
