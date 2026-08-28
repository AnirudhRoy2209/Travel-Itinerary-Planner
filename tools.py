from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
load_dotenv()
import os
import requests

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query:str)->list:
    """Searches the live web for travel guides, local events, attractions, and activities in a given destination. Use this to find recent, relevant URLs for travel planning."""
    result=tavily.search(
        query=query,
        max_results=3
    )

    out=[]

    for items in result["results"]:
       out.append(items["url"])
    return out

@tool
def scrape_page(url:str)->str:
    """Fetches and extracts clean, readable text content from a specific webpage URL. Use this to read the details, schedules, pricing, and descriptions from a URL found via search."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response=requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"cannot access the url:{e}")
        return ""
    soup=BeautifulSoup(response.text, "html.parser")
    for i in soup(["script", "style", "nav", "footer"]):
        i.decompose()
    return soup.get_text(separator=" ", strip=True)
