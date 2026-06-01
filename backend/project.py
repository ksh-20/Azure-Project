import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

organization = os.getenv("AZURE_ORG")
project = os.getenv("AZURE_PROJECT")
pat = os.getenv("AZURE_PAT")


def fetch_projects():
    url = f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url=url, auth=auth)

    if response.status_code != 200:
         return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    
    projects = []

    for project in response.json()["value"]:
         projects.append({
            "id": project["id"],
            "name": project["name"],
            "description": project.get("description"),
            "state": project["state"],
            "visibility": project["visibility"],
            "url": project["url"]
        })

    return {
        "success": True,
        "count": len(projects),
        "projects": projects
    }