from dataclasses import dataclass
from fastapi import FastAPI

app = FastAPI()

COMMITS = {}

@dataclass
class Commit:
    sha: str
    tests_ok: bool | None = None
    build_ok: bool | None = None
    deploy_ok: bool | None = None


@app.get("/{sha}/status")
async def get_status(sha: str) -> Commit:

    return COMMITS.get(sha, Commit(sha=sha))

@app.post("/{sha}/test")
async def test_commit(sha: str, tests_ok: bool) -> Commit:
    commit = COMMITS.get(sha, Commit(sha=sha))
    commit.tests_ok = tests_ok
    COMMITS[commit.sha] = commit
    return commit

@app.post("/{sha}/build")
async def build_commit(sha: str, build_ok: bool) -> Commit:
    commit = COMMITS.get(sha, Commit(sha=sha))
    commit.build_ok = build_ok
    COMMITS[commit.sha] = commit
    return commit

@app.post("/{sha}/deploy")
async def deploy_commit(sha: str, deploy_ok: bool) -> Commit:
    commit = COMMITS.get(sha, Commit(sha=sha))
    commit.deploy_ok = deploy_ok
    COMMITS[commit.sha] = commit
    return commit