from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Template

with open("index.jinja2") as f:
    template = Template(f.read())


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

@app.get("/", response_class=HTMLResponse)
async def show_all_commits():
    return template.render(commits=COMMITS.values())

@app.post("/{sha}/test")
async def test_commit(sha: str, tests_ok: bool) -> Commit:
    commit = COMMITS.get(sha, Commit(sha=sha))
    commit.tests_ok = tests_ok
    COMMITS[commit.sha] = commit
    return commit


@app.post("/{sha}/deploy")
async def deploy_commit(sha: str, deploy_ok: bool) -> Commit:
    commit = COMMITS.get(sha, Commit(sha=sha))
    commit.deploy_ok = deploy_ok
    COMMITS[commit.sha] = commit
    return commit