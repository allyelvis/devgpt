from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth.github_oauth import router as auth_router
from api.github.repo_handler import router as github_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(github_router, prefix="/github")
