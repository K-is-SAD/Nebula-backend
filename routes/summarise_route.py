from fastapi import APIRouter
from controllers import summarise as summarise_controller
from pydantic import BaseModel

router = APIRouter()

class GithubRepo(BaseModel):
    github_repo_url : str

@router.post("/api/summarise")
async def summarise(repo: GithubRepo):
    print(f"Received GitHub URL: {repo.github_repo_url}")
    result = {}
    if repo.github_repo_url == None or repo.github_repo_url == "":
        result = {
            "error": "No GitHub URL provided.",
            "success": False
        }
        return result
    else:
        result = await summarise_controller.run_pipeline(github_url=repo.github_repo_url)
        print(f"Result: {result}")

    return result