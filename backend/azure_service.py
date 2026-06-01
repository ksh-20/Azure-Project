import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

organization = os.getenv("AZURE_ORG")
project = os.getenv("AZURE_PROJECT")
pat = os.getenv("AZURE_PAT")


def fetch_repositories():
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

    data = response.json()

    repos = [
        {
            "id": repo["id"],
            "name": repo["name"],
            "project": repo["project"]["name"],
            "remoteUrl": repo["remoteUrl"],
            "defaultBranch": repo.get("defaultBranch")
        }
        for repo in data["value"]
    ]

    return {
        "success": True,
        "count": len(repos),
        "repositories": repos
    }