from fastapi import FastAPI, HTTPException
from app.database import init_db, get_connection
from app.github import fetch_open_issues
from app.llm import analyze_issues

app = FastAPI(title="GitHub Issue Analyzer")


# ------------------------
# Startup: initialize DB
# ------------------------
@app.on_event("startup")
def startup():
    init_db()


# ------------------------
# Health check
# ------------------------
@app.get("/")
def root():
    return {"status": "API is running"}


# ------------------------
# POST /scan
# ------------------------
@app.post("/scan")
async def scan_repo(payload: dict):
    repo = payload.get("repo")

    if not repo:
        raise HTTPException(status_code=400, detail="repo is required")

    try:
        issues = await fetch_open_issues(repo)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch issues: {str(e)}"
        )

    conn = get_connection()
    cursor = conn.cursor()

    for issue in issues:
        cursor.execute("""
            INSERT OR REPLACE INTO issues
            (id, repo, title, body, html_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            issue["id"],
            repo,
            issue["title"],
            issue.get("body", ""),
            issue["html_url"],
            issue["created_at"]
        ))

    conn.commit()
    conn.close()

    return {
        "repo": repo,
        "issues_fetched": len(issues),
        "cached_successfully": True
    }


# ------------------------
# POST /analyze
# ------------------------
@app.post("/analyze")
def analyze_repo(payload: dict):
    repo = payload.get("repo")
    prompt = payload.get("prompt")

    if not repo or not prompt:
        raise HTTPException(
            status_code=400,
            detail="repo and prompt are required"
        )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, body FROM issues WHERE repo = ?",
        (repo,)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No cached issues found for this repo. Run /scan first."
        )

    issues_text = [
        f"Title: {title}\nBody: {body or ''}"
        for title, body in rows
    ]

    try:
        analysis = analyze_issues(prompt, issues_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM analysis failed: {str(e)}"
        )

    return {
        "analysis": analysis
    }

# ------------------------
# POST /issues/list
# ------------------------
@app.post("/issues/list")
def list_issues_detailed(payload: dict):
    repo = payload.get("repo")

    if not repo:
        raise HTTPException(
            status_code=400,
            detail="repo is required"
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, body, html_url, created_at
        FROM issues
        WHERE repo = ?
        ORDER BY created_at DESC
    """, (repo,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No cached issues found. Run /scan first."
        )

    issues = []
    for row in rows:
        issues.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "url": row[3],
            "created_at": row[4]
        })

    return {
        "repo": repo,
        "total_issues": len(issues),
        "issues": issues
    }
