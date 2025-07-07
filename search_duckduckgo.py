import requests
from bs4 import BeautifulSoup
from utils import get_user_agent
from keywords import keywords

def search_duckduckgo():
    results = []
    for query in keywords:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": get_user_agent()}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        for result in soup.select("a.result__a"):
            title = result.get_text()
            link = result.get("href")
            if link and "duckduckgo.com/y.js" not in link:
                results.append({"title": title, "url": link, "source": "duckduckgo"})
    return results