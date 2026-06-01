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


def fetch_files(repo_id):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/items?recursionLevel=Full&api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    print("Status:", response.status_code)
    print("Headers:", response.headers.get("Content-Type"))
    print("Response:")
    print(response.text)

    return response.text


def fetch_commits(repo_id):
    url = url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/commits?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return response.json()
    
    commits = []
    
    for commit in response.json()["value"]:
        commits.append({
            "commitId" : commit["commitId"],
            "author" : commit["author"]["name"],
            "email" : commit["author"]["email"],
            "date" : commit["author"]["date"],
            "comment" : commit.get("comment")
        })

    return commits


def fetch_pushes(repo_id):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/pushes?api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return response.json
    
    pushes = []

    for push in response.json()["value"]:
        pushes.append({
            "pushId" : push["pushId"],
            "date" : push["date"],
            "pushedBy" : push["pushedBy"]["displayName"]
        })

    return pushes


def fetch_branches(repo_id):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/refs?filter=heads/&api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return response.json()
    
    branches = []

    for branch in response.json()["value"]:
        branches.append({
            "name" : branch["name"],
            "objectId" : branch["objectId"]
        })

    return branches


def fetch_tags(repo_id):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/refs?filter=tags/&api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return response.json()
    
    tags = []

    for tag in response.json()["value"]:
        tags.append({
            "name" : tag["name"],
            "objectId" : tag["objectId"]
        })

    return tags


def fetch_pull_requests(repo_id):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repo_id}/pullrequests?searchCriteria.status=all&api-version=7.1"
    auth = HTTPBasicAuth("", pat)

    response = requests.get(url=url, auth=auth)

    if response.status_code != 200:
        return response.json()
    
    prs = []

    for pr in response.json()["value"]:
        prs.append({
            "pullRequestId": pr["pullRequestId"],
            "title": pr["title"],
            "status": pr["status"],
            "createdBy": pr["createdBy"]["displayName"],
            "creationDate": pr["creationDate"],
            "sourceBranch": pr["sourceRefName"],
            "targetBranch": pr["targetRefName"]
        })

    return prs



# Below is for testing the functions only. Use Flask API endpoints to test for integration

res = fetch_repositories()
for key in res:
    print(key, ":", res[key])

print(fetch_files("968d7613-f79f-4b56-80e9-c6ccccda13d8"))