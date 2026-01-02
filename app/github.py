import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def fetch_open_issues(repo: str):
    owner, name = repo.split("/")
    issues = []
    page = 1

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(
                f"{GITHUB_API}/repos/{owner}/{name}/issues",
                params={"state": "open", "per_page": 100, "page": page},
                headers=headers
            )

            if response.status_code != 200:
                raise RuntimeError(response.text)

            data = response.json()
            if not data:
                break

            for issue in data:
                if "pull_request" not in issue:
                    issues.append(issue)

            page += 1

    return issues
