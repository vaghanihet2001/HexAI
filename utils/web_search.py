import requests
from duckduckgo_search import DDGS

def duckduckgo_search(query: str, max_results: int = 5):
    with DDGS() as ddgs:
        results = [r["title"] + " - " + r["href"] for r in ddgs.text(query, max_results=max_results)]
    return results

def should_search_web(user_input: str, rag_results: str) -> bool:
    # If RAG returns very little or empty
    if not rag_results.strip():
        return True
    # If input contains keywords like "latest", "current", "today"
    search_keywords = ["latest", "current", "today", "news", "update","search"]
    if any(k in user_input.lower() for k in search_keywords):
        return True
    return False


def search_web(query: str, max_results: int = 50) -> str:
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
        
    }
    try:
        resp = requests.get(url, params=params)

        data = resp.json()
        print("data",data)
        # DuckDuckGo has 'AbstractText' and 'RelatedTopics'
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if "Text" in topic:
                results.append(topic["Text"])
        if data.get("Answer"):
            results.append(data["Answer"])
        return "\n".join(results)
    except Exception as e:
        print("❌ Web search error:", e)
        return "No results found."

if __name__ == "__main__":
    print(duckduckgo_search("today's gold rate in ahmedabad in rupees?"))