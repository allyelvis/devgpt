from fastapi import APIRouter
from pydantic import BaseModel
import subprocess

router = APIRouter()

class ExecRequest(BaseModel):
    code: str
    language: str

@router.post("/")
def run_code(req: ExecRequest):
    try:
        if req.language == "python":
            result = subprocess.run(["python3", "-c", req.code], capture_output=True, text=True, timeout=5)
        elif req.language == "node":
            result = subprocess.run(["node", "-e", req.code], capture_output=True, text=True, timeout=5)
        else:
            return {"output": "Unsupported language"}
        return {"output": result.stdout or result.stderr}
    except Exception as e:
        return {"output": str(e)}
