from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
import requests, os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
CID = os.getenv("GITHUB_CLIENT_ID")
CSEC = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:3000/auth/callback")

@router.get("/login")
def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={CID}&redirect_uri={REDIRECT_URI}&scope=repo"
    )

@router.get("/callback")
def callback(code: str, response: Response):
    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={"client_id": CID, "client_secret": CSEC, "code": code}
    ).json()
    token = token_resp.get("access_token")
    response.set_cookie("github_token", token, httponly=True, samesite="lax")
    return RedirectResponse("/")
