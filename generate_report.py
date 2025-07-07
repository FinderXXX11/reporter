from datetime import date
import os
from urllib.parse import urlparse
from translate_titles import translate_to_polish

CATEGORY_MAP = {
    "mil.ru": "Rosja",
    "tass.ru": "Rosja",
    "topwar.ru": "Rosja",
    "redstar.ru": "Rosja",
    "tvzvezda.ru": "Rosja",
    "ria.ru": "Rosja",
    "belta.by": "Białoruś",
    "naviny.online": "Białoruś",
    "ukrinform.ua": "Ukraina",
    "unian.net": "Ukraina",
    "defence-ua.com": "Ukraina",
    "mil.in.ua": "Ukraina",
    "kyivindependent.com": "Ukraina",
    "reutersagency.com": "Międzynarodowe",
    "aljazeera.com": "Międzynarodowe",
    "defence-blog.com": "Międzynarodowe",
    "nato.int": "NATO",
    "understandingwar.org": "Międzynarodowe"
}

def extract_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "").lower()
    except:
        return "nieznane"

def categorize_by_source(domain):
    return CATEGORY_MAP.get(domain, "Inne")

def generate_html_report(results):
    today = date.today().isoformat()
    for r in results:
        r["domain"] = extract_domain(r["url"])
        r["category"] = categorize_by_source(r["domain"])
        r["published"] = r.get("published", "")
        r["published_source"] = r.get("published_source", "nieznana")

    sorted_results = sorted(results, key=lambda x: (x["category"], x["domain"], x["published"]))

    html = "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Raport {}</title></head><body>".format(today)
    html += "<h1>Raport dzienny – {}</h1>".format(today)

    categories = sorted(set(r["category"] for r in sorted_results))
    for cat in categories:
        html += f"<h2>{cat}</h2><ol>"
        for r in sorted_results:
            if r["category"] != cat:
                continue
            translated = translate_to_polish(r['title'])
            timestamp = r['published'] if r['published'] else "brak danych"
            origin = r['published_source'] if r['published_source'] != "none" else "nieznana"
            html += f"<li><a href='{r['url']}'>{r['title']}</a><br>"
            html += f"<i>{translated}</i><br>"
            html += f"<b>Źródło:</b> {r['domain']} &nbsp;&nbsp; "
            html += f"<b>Data publikacji:</b> {timestamp} (<i>{origin}</i>)</li>"
        html += "</ol>"

    html += "</body></html>"

    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{today}.html", "w", encoding="utf-8") as f:
        f.write(html)