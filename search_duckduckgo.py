import requests
from bs4 import BeautifulSoup
from utils import get_user_agent
from keywords import keywords
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs

def parse_date(raw_date):
    formats = [
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(raw_date, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            continue
    return ""

def try_extract_date_from_snippet(snippet):
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{1,2}[./]\d{1,2}[./]\d{4})"
    ]
    for pattern in patterns:
        match = re.search(pattern, snippet)
        if match:
            parsed = parse_date(match.group(0))
            if parsed:
                return parsed, "snippet"
    return "", "none"

def try_extract_date_from_page(url):
    try:
        headers = {"User-Agent": get_user_agent()}
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")

        time_tag = soup.find("time")
        if time_tag and time_tag.has_attr("datetime"):
            parsed = parse_date(time_tag["datetime"][:19])
            if parsed:
                return parsed, "meta-time"

        meta_date = soup.find("meta", attrs={"name": "date"})
        if meta_date and meta_date.has_attr("content"):
            parsed = parse_date(meta_date["content"][:19])
            if parsed:
                return parsed, "meta-date"
    except:
        pass
    return "", "none"

def clean_duckduckgo_link(href):
    if "/l/?kh=" in href and "uddg=" in href:
        parsed = parse_qs(urlparse(href).query)
        if "uddg" in parsed:
            return parsed["uddg"][0]
    return href

def search_duckduckgo():
    results = []
    for query in keywords:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": get_user_agent()}
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        for result in soup.select("div.result"):
            link_tag = result.select_one("a.result__a")
            snippet_tag = result.select_one("a.result__snippet")
            if not link_tag:
                continue

            title = link_tag.get_text()
            raw_link = link_tag.get("href")
            link = clean_duckduckgo_link(raw_link)

            if link and "duckduckgo.com/y.js" not in link:
                snippet = snippet_tag.get_text() if snippet_tag else ""
                published, published_source = try_extract_date_from_snippet(snippet)
                if not published:
                    published, published_source = try_extract_date_from_page(link)

                results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "published": published,
                    "published_source": published_source
                })
    return results