from langchain_community.tools.tavily_search import TavilySearchResults
import json
from langchain_core.tools import tool

from dotenv import load_dotenv
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"  #I don't have an API key for the tracing service, so turn off tracing to avoid errors for now


load_dotenv(".env")
load_dotenv(".secrets")

# Returns structured results; we’ll wrap it to return a string
tavily_tool = TavilySearchResults(max_results=5,tavily_api_key=os.environ["TAVILY_API_KEY"])



@tool
def web_search(query: str) -> str:
    """Search the web (Tavily) and return top results with title, url, and snippet."""
    results = tavily_tool.invoke({"query": query})
    # results is usually a list of dicts with keys like title/url/content
    lines = []
    for i, r in enumerate(results, start=1):
        title = r.get("title", "").strip()
        url = r.get("url", "").strip()
        snippet = (r.get("content") or r.get("snippet") or "").strip()
        lines.append(f"{i}. {title}\n{url}\n{snippet}")
    return "\n\n".join(lines) if lines else "No results found."