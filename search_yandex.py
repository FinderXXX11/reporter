import requests
from bs4 import BeautifulSoup
from utils import get_user_agent
from keywords import keywords

def search_yandex():
    results = []
    for query in keywords:
        url = f"https://yandex.ru/search/?text={query}"
        headers = {"User-Agent": get_user_agent()}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.select("a.Link"):
            title = a.get_text()
            link = a.get("href")
            if link and link.startswith("http"):
                results.append({"title": title, "url": link, "source": "yandex"})
    return results