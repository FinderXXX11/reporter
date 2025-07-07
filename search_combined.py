import requests
from bs4 import BeautifulSoup
from utils import get_user_agent
from keywords import keywords
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, unquote
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
            for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"]:
                try:
                    dt = datetime.strptime(match.group(0), fmt)
                    return dt.strftime("%Y-%m-%d %H:%M"), "pattern", dt
                except:
                    continue
    return "", "none", None

def search_yandex():
    results = []
    headers = {"User-Agent": get_user_agent(), "Accept-Language": "ru,en;q=0.9"}
    cutoff = datetime.now() - timedelta(days=2)
    for q in keywords:
        url = f"https://yandex.ru/search/?text={q}&lr=213&from_day=2"
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
                published, src, pub_dt = parse_date_generic(snippet)
                if pub_dt and pub_dt < cutoff:
                    continue
                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": published,
                    "published_source": src,
                    "domain": extract_domain(link),
                    "engine": "Yandex"
                })
        except Exception:
            continue
    return results

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "u" in qs:
        return unquote(qs["u"][0])
    return url


def search_rss():
    import feedparser
    feeds = [
        "https://function.mil.ru/rss.xml",
        "https://tass.ru/rss/v2.xml",
        "https://topwar.ru/rss.xml",
        "https://redstar.ru/feed/",
        "https://tvzvezda.ru/rss.xml",
        "https://ria.ru/export/rss2/politics/index.xml",
        "https://www.belta.by/rss/politics.rss",
        "https://naviny.online/rss.xml",
        "https://www.ukrinform.ua/rubric-defense.rss",
        "https://www.unian.net/rss/publications/unian.rss",
        "https://defence-ua.com/rss.html",
        "https://mil.in.ua/uk/feed/",
        "https://www.reutersagency.com/feed/?best-sectors=conflict",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://defence-blog.com/feed/",
        "https://www.nato.int/cps/en/natohq/news_rss.htm",
        "https://kyivindependent.com/feed",
        "https://understandingwar.org/rss.xml"
    ]
    results = []
    cutoff = datetime.now() - timedelta(days=2)
    for url in feeds:
        d = feedparser.parse(url)
        for entry in d.entries:
            title = entry.title
            link = entry.link
            snippet = entry.get("summary", "")
            try:
                dt = datetime(*entry.published_parsed[:6])
                if dt < cutoff:
                    continue
                published = dt.strftime("%Y-%m-%d %H:%M")
                src = "rss"
            except:
                published = ""
                src = "none"
            results.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "published": published,
                "published_source": src,
                "domain": extract_domain(link),
                "engine": "RSS"
            })
    return results

def search_all_sources():
    return search_yandex() + search_rss()