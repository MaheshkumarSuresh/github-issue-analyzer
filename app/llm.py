# def analyze_issues(prompt: str, issues: list[str]) -> str:
#     combined_prompt = f"""
# You are analyzing GitHub issues.

# User request:
# {prompt}

# Issues:
# {chr(10).join(issues[:10])}
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You analyze GitHub issues."},
#                 {"role": "user", "content": combined_prompt}
#             ],
#             temperature=0.3
#         )
#         return response.choices[0].message.content

#     except Exception:
#         # API Limit exceed error due to free version
#         return (
#             " LLM quota exceeded. Fallback analysis:\n\n"
#             "Based on the cached issues, several recurring themes appear:\n"
#             "- Documentation clarity and missing examples\n"
#             "- Edge cases in async behavior\n"
#             "- Feature requests around configuration flexibility\n\n"
#             "Maintainers should prioritize issues that block core usage "
#             "and improve documentation, as these impact the largest number of users."
#         )

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_issues(prompt: str, issues: list[str]) -> str:
    combined_issues = "\n\n".join(issues)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a senior software engineer analyzing GitHub issues."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nIssues:\n{combined_issues}"
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
