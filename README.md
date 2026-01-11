# GitHub Issue Analyzer with Local Caching + LLM Processing

## Overview
This project is a small backend service built as part of a coding assignment. It provides two REST API endpoints that:

1. Fetch and locally cache open GitHub issues for a repository
2. Analyze the cached issues using a natural-language prompt and an LLM

The service is designed to be simple, demo-friendly, and production-aware, with clear error handling and persistence.

---

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **HTTP Client**: httpx
- **Database**: SQLite
- **LLM Provider**: OpenAI API (with graceful fallback when quota is unavailable)

---

## Why SQLite for Local Caching

SQLite was chosen as the local storage option because:

- It is **persistent** (data survives server restarts)
- It requires **no external database setup**
- It is easy to inspect and debug during interviews
- It scales better than JSON files for growing datasets

This makes SQLite a good balance between simplicity and durability for this assignment.

---

## Project Structure

```
github-issue-analyzer/
├── app/
│   ├── main.py        # FastAPI application and endpoints
│   ├── database.py    # SQLite connection and initialization
│   ├── github.py      # GitHub API integration
│   └── llm.py         # LLM analysis logic
│
├── issues.db          # SQLite database (auto-created)
├── requirements.txt  # Python dependencies
├── README.md
└── .env               # Environment variables (not committed)
```

---

## Setup & Running the Server

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Set Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here (optional)
GROQ_API_KEY=your_grooq_api_key_here
GITHUB_TOKEN=your_github_token_here
```

- `OPENAI_API_KEY` is used for LLM-based analysis
- `GITHUB_TOKEN` is optional but recommended to avoid GitHub API rate limits

> Note: If the OpenAI quota is exceeded or unavailable, the application falls back to a mock analysis so the demo still works.

### 3. Run the Server

```bash
python -m uvicorn app.main:app --reload
```

The server will start at:
```
http://127.0.0.1:8000
```

Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### 1. POST /scan

**Purpose**  
Fetch all open issues from a GitHub repository and cache them locally.

**Request**
```json
{
  "repo": "owner/repository-name"
}
```

**Behavior**
- Fetches all open issues from GitHub REST API
- Filters out pull requests
- Stores issue data in SQLite

**Response**
```json
{
  "repo": "owner/repository-name",
  "issues_fetched": 42,
  "cached_successfully": true
}
```

---

### 2. POST /analyze

**Purpose**  
Analyze cached issues using a natural-language prompt and an LLM.

**Request**
```json
{
  "repo": "owner/repository-name",
  "prompt": "Find themes across recent issues and recommend what the maintainers should fix first"
}
```

**Behavior**
- Retrieves cached issues from SQLite
- Combines the user prompt with issue data
- Sends the context to an LLM for analysis
- Returns a natural-language summary

**Response**
```json
{
  "analysis": "<LLM-generated analysis text>"
}
```

**Edge Cases Handled**
- Repo not scanned yet
- No cached issues
- GitHub API errors
- LLM quota or API errors (graceful fallback)

---

## AI Prompts Used

### Prompts Sent to AI Coding Tools

- "Create a FastAPI backend with SQLite persistence"
- "Implement a GitHub issues fetcher with pagination"
- "Design an endpoint to analyze cached GitHub issues using an LLM"
- "Fix FastAPI startup and SQLite initialization issues"

### Prompts Used to Design / Debug Code

- "How to filter pull requests from GitHub issues API"
- "Handle OpenAI API quota errors gracefully"
- "Improve error handling for missing cached data"

### Prompt Used Inside the Analyze Endpoint

```
You are analyzing GitHub issues for a repository.

User request:
{user_prompt}

Issues:
{list_of_cached_issues}

Provide a clear, concise analysis highlighting recurring themes and recommendations.
```

---

## Notes for Demo & Interview

- The service is fully functional without a UI
- SQLite ensures cached data persists across restarts
- LLM failures do not break the API (fallback analysis is returned)
- The architecture is intentionally simple and easy to explain

---

## Future Improvements (Optional)

- Chunking large issue sets to handle context limits
- Caching LLM responses
- Authentication for private repositories
- Support for additional LLM providers

---

## License

This project is created solely for evaluation purposes as part of a technical interview assignment.
