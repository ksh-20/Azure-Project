import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

organization = os.getenv("AZURE_ORG")
project = os.getenv("AZURE_PROJECT")
pat = os.getenv("AZURE_PAT")


def fetch_work_item_ids():
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    query = {
        "query": """
        SELECT [System.Id]
        FROM WorkItems
        ORDER BY [System.ChangedDate] DESC
        """
    }

    response = requests.post(url, json=query, auth=auth)

    if response.status_code != 200:
        return []

    return [item["id"] for item in response.json()["workItems"]]


def fetch_work_items(project):
    ids = fetch_work_item_ids(project)

    if not ids:
        return {
            "success": False,
            "message": "No work items found"
        }

    ids_string = ",".join(map(str, ids[:100]))

    url = f"https://dev.azure.com/{organization}/_apis/wit/workitems?ids={ids_string}&api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

    work_items = []

    for item in response.json()["value"]:
        fields = item["fields"]

        work_items.append({
            "id": item["id"],
            "title": fields.get("System.Title"),
            "type": fields.get("System.WorkItemType"),
            "state": fields.get("System.State"),
            "assignedTo": fields.get("System.AssignedTo", {}).get("displayName")
                if isinstance(fields.get("System.AssignedTo"),dict)
                else None,
            "createdDate": fields.get("System.CreatedDate")
        })

    return {
        "success": True,
        "count": len(work_items),
        "workItems": work_items
    }