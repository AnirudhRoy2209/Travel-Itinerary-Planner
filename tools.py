import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()


def get_tavily_key() -> str:
    """Fetch TAVILY_API_KEY from Streamlit Secrets first, then os.environ."""
    try:
        if "TAVILY_API_KEY" in st.secrets:
            return str(st.secrets["TAVILY_API_KEY"]).strip()
    except Exception:
        pass
    return (os.getenv("TAVILY_API_KEY") or "").strip()


@tool
def web_search(query: str) -> list:
    """Searches the live web for travel guides, local events, attractions, and activities in a given destination. Use this to find recent, relevant URLs for travel planning."""
    api_key = get_tavily_key()
    if not api_key:
        raise ValueError(
            "Missing TAVILY_API_KEY! Add TAVILY_API_KEY = 'tvly-...' to your Streamlit Cloud Secrets."
        )

    tavily = TavilyClient(api_key=api_key)
    result = tavily.search(query=query, max_results=3)

    return [item["url"] for item in result.get("results", [])]


@tool
def scrape_page(url: str) -> str:
    """Fetches and extracts clean, readable text content from a specific webpage URL. Use this to read the details, schedules, pricing, and descriptions from a URL found via search."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"cannot access the url: {e}")
        return f"Could not access {url}: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    # Cap text length so huge web pages don't blow past Groq's TPM limit
    return text[:1800]
