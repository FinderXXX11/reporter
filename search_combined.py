import requests
from bs4 import BeautifulSoup
from utils import get_user_agent
from keywords import keywords
from datetime import datetime, timedelta
from urllib.parse import urlparse
import re

def extract_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return "nieznane"

def parse_date_generic(text):
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{1,2}[./-]\d{1,2}[./-]\d{4})",
        r"(\d{4}/\d{2}/\d{2})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"]:
                    try:
                        dt = datetime.strptime(match.group(0), fmt)
                        return dt.strftime("%Y-%m-%d %H:%M"), "pattern"
                    except:
                        continue
            except:
                pass
    return "", "none"

def search_yandex():
    results = []
    headers = {
        "User-Agent": get_user_agent(),
        "Accept-Language": "ru,en;q=0.9",
    }
    for q in keywords:
        url = f"https://yandex.ru/search/?text={q}&from_day=2"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for block in soup.select("li.serp-item"):
                a = block.find("a", href=True)
                if not a:
                    continue
                title = a.get_text(strip=True)
                link = a["href"]
                snippet = block.get_text()
                published, src = parse_date_generic(snippet)
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": published,
                    "published_source": src,
                    "domain": extract_domain(link),
                    "engine": "Yandex"
                })
        except Exception as e:
            continue
    return results

def search_bing():
    results = []
    headers = {"User-Agent": get_user_agent()}
    for q in keywords:
        url = f"https://www.bing.com/search?q={q}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for li in soup.select("li.b_algo"):
                a = li.find("a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                link = a["href"]
                snippet = li.get_text()
                published, src = parse_date_generic(snippet)
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": published,
                    "published_source": src,
                    "domain": extract_domain(link),
                    "engine": "Bing"
                })
        except:
            continue
    return results

def search_rss():
    import feedparser
    feeds = [
        "https://topwar.ru/rss.xml",
        "https://function.mil.ru/rss.xml",
        "https://ria.ru/export/rss2/politics/index.xml",
        "https://tass.ru/rss/v2.xml"
    ]
    results = []
    for url in feeds:
        d = feedparser.parse(url)
        for entry in d.entries[:20]:
            title = entry.title
            link = entry.link
            snippet = entry.get("summary", "")
            published = entry.get("published", "")
            try:
                dt = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                src = "rss"
            except:
                dt = ""
                src = "none"
            results.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "published": dt,
                "published_source": src,
                "domain": extract_domain(link),
                "engine": "RSS"
            })
    return results

def search_all_sources():
    return search_yandex() + search_bing() + search_rss()