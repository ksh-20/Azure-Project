import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

organization = os.getenv("AZURE_ORG")
project = os.getenv("AZURE_PROJECT")
pat = os.getenv("AZURE_PAT")


def fetch_pipelines():
    url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url=url, auth=auth)

    if response.status_code != 200:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.json()
        }
    
    pipelines = []

    for pipeline in response.json()["value"]:
        pipelines.append({
            "id" : pipeline["id"],
            "name" : pipeline["name"],
            "folder" : pipeline.get("folder")
        })

    return {
        "success" : True,
        "count" : len(pipelines),
        "pipelines" : pipelines
    }