from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from repository import (
    fetch_repositories,
    fetch_files,
    fetch_commits,
    fetch_pushes,
    fetch_branches,
    fetch_tags,
    fetch_pull_requests
)
from project import fetch_projects
from pipelines import fetch_pipelines

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/projects")
async def get_projects():
    result = fetch_projects()
    return result

@app.get("/api/repos")
async def get_repositories():
    result = fetch_repositories()
    return result

@app.get("/api/repos/{repo_id}/files")
async def get_files(repo_id: str):
    return fetch_files(repo_id)

@app.get("/api/repos/{repo_id}/commits")
async def get_commits(repo_id: str):
    return fetch_commits(repo_id)

@app.get("/api/repos/{repo_id}/pushes")
async def get_pushes(repo_id: str):
    return fetch_pushes(repo_id)

@app.get("/api/repos/{repo_id}/branches")
async def get_branches(repo_id: str):
    return fetch_branches(repo_id)

@app.get("/api/repos/{repo_id}/tags")
async def get_tags(repo_id: str):
    return fetch_tags(repo_id)

@app.get("/api/repos/{repo_id}/pullrequests")
async def get_pull_requests(repo_id: str):
    return fetch_pull_requests(repo_id)

@app.get("/api/pipelines")
async def get_pipelines():
    result = fetch_pipelines()
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)