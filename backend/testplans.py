import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

organization = os.getenv("AZURE_ORG")
project = os.getenv("AZURE_PROJECT")
pat = os.getenv("AZURE_PAT")


def fetch_test_plans():
    url = f"https://dev.azure.com/{organization}/{project}/_api/testplan/plans/?api-version=7.1-preview.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url=url, auth=auth)

    if response.status_code != 200:
         return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    
    plans = []

    for plan in response.json()["value"]:
        plans.append({
            "id": plan["id"],
            "name": plan["name"],
            "state": plan["state"],
            "areaPath": plan.get("areaPath"),
            "iteration": plan.get("iteration")
        })

    return {
        "success" : True,
        "count" : len(plans),
        "plans" : plans
    }