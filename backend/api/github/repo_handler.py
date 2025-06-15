from fastapi import APIRouter, Cookie, HTTPException
from github import Github
from pydantic import BaseModel

router = APIRouter()

@router.get("/repos")
def get_repos(github_token: str = Cookie(None)):
    if not github_token:
        raise HTTPException(status_code=401, detail="Login required")
    g = Github(github_token)
    return [repo.full_name for repo in g.get_user().get_repos() if not repo.fork]

@router.get("/repos/{owner}/{repo}/contents/{path:path}")
def get_file(owner: str, repo: str, path: str, github_token: str = Cookie(None)):
    if not github_token:
        raise HTTPException(status_code=401, detail="Login required")
    gh = Github(github_token)
    file = gh.get_repo(f"{owner}/{repo}").get_contents(path)
    return {"path": file.path, "content": file.decoded_content.decode()}

class CommitReq(BaseModel):
    owner: str
    repo: str
    path: str
    content: str
    message: str

@router.post("/repos/commit")
def commit_file(req: CommitReq, github_token: str = Cookie(None)):
    if not github_token:
        raise HTTPException(status_code=401, detail="Login required")
    gh = Github(github_token)
    repo = gh.get_repo(f"{req.owner}/{req.repo}")
    existing = repo.get_contents(req.path)
    repo.update_file(req.path, req.message, req.content, existing.sha)
    return {"status": "committed"}
