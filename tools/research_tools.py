from pathlib import Path
from duckduckgo_search import DDGS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "healthcare_ai_notes.txt"

def guardrail_check(user_query: str) -> dict:
    """
    Check whether the user's query is safe for this demo.
    Always call this first before doing research.

    Returns:
        dict: status, reason, and safe_response fields.
    """
    q = user_query.lower()

    restricted_patterns = [
        "diagnose me",
        "what disease do i have",
        "prescribe",
        "dosage",
        "medical advice for me",
        "treatment for me personally",
        "my symptoms mean",
    ]

    for pattern in restricted_patterns:
        if pattern in q:
            return {
                "status": "restricted",
                "reason": "The query asks for personal medical advice or diagnosis.",
                "safe_response": (
                    "I can provide general educational information, but I cannot "
                    "diagnose conditions or give personal medical advice. "
                    "Please consult a qualified healthcare professional."
                ),
            }

    return {
        "status": "allowed",
        "reason": "General educational or research request.",
        "safe_response": "",
    }


def research_framework(topic: str) -> dict:
    """
    Return a structured framework for researching the topic.
    Always call this before drafting the research findings.
    """
    topic_lower = topic.lower()

    if "health" in topic_lower or "medical" in topic_lower:
        return {
            "focus_areas": [
                "clinical applications",
                "administrative applications",
                "benefits and opportunities",
                "risks and limitations",
                "ethics and privacy concerns",
                "real-world examples",
            ],
            "recommended_output": [
                "short executive summary",
                "bullet point findings",
                "clear conclusion",
            ],
            "audience": "general non-technical audience",
        }

    return {
        "focus_areas": [
            "definition",
            "key use cases",
            "benefits",
            "limitations",
            "examples",
            "future outlook",
        ],
        "recommended_output": [
            "short executive summary",
            "bullet point findings",
            "clear conclusion",
        ],
        "audience": "general audience",
    }


def local_reference_lookup(query: str) -> dict:
    """
    Look up curated internal healthcare AI notes from a local file.

    Args:
        query: The user topic or question.

    Returns:
        A dictionary with the query and the relevant local notes.
    """
    file_path = DATA_FILE

    if not file_path.exists():
        return {
            "status": "error",
            "topic": query,
            "notes": "Local reference file not found."
        }

    content = file_path.read_text(encoding="utf-8")

    return {
        "status": "ok",
        "topic": query,
        "notes": content
    }

def web_search_tool(query: str) -> dict:
    """
    Perform a simple web search using DuckDuckGo.

    Returns top search results with title and snippet.
    """

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=5)

            for r in search_results:
                results.append({
                    "title": r.get("title"),
                    "snippet": r.get("body"),
                    "url": r.get("href")
                })

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "results": []
        }

    return {
        "status": "ok",
        "query": query,
        "results": results
    }