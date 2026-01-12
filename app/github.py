import httpx
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def fetch_open_issues(repo: str):
    owner, name = repo.split("/")
    issues = []
    since = None  # cursor

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        while True:
            params = {
                "state": "open",
                "per_page": 100
            }

            if since:
                params["since"] = since

            response = await client.get(
                f"{GITHUB_API}/repos/{owner}/{name}/issues",
                headers=headers,
                params=params
            )

            if response.status_code != 200:
                raise RuntimeError(response.text)

            data = response.json()
            if not data:
                break

            # Filter out pull requests
            page_issues = [i for i in data if "pull_request" not in i]
            issues.extend(page_issues)

            # Cursor = last issue updated time
            since = data[-1]["updated_at"]

    return issues
