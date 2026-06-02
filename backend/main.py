from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from repository import fetch_repositories
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

@app.get("/api/pipelines")
async def get_pipelines():
    result = fetch_pipelines()
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)