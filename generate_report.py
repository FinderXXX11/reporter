from datetime import date
import os
from urllib.parse import urlparse
from translate_titles import translate_to_polish

def extract_domain(url):
    try:
        netloc = urlparse(url).netloc
        domain = netloc.replace("www.", "").split("/")[0]
        return domain
    except:
        return "nieznane źródło"

# Kategorie i słowa kluczowe
CATEGORIES = {
    "Ćwiczenia i szkolenia": ["учения", "тренировка", "подготовка", "тактические", "манёвры", "боеготовность"],
    "Modernizacja sprzętu": ["модернизация", "техника", "вооружение", "ракета", "поставка", "доставка", "новая система"],
    "Zmiany kadrowe": ["назначен", "уволен", "командующий", "генерал", "перемещения", "кадровые"]
}

def categorize(text_ru):
    text_lower = text_ru.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in text_lower:
                return category
    return "Inne"

def generate_html_report(results):
    today = date.today().isoformat()
    for r in results:
        r["domain"] = extract_domain(r["url"])
        r["published"] = r.get("published", "")
        r["published_source"] = r.get("published_source", "nieznana")
        r["category"] = categorize(r["title"])

    sorted_results = sorted(results, key=lambda x: (x["category"], x["domain"], x["published"]))

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Raport {today}</title></head><body>
<h1>Raport dzienny – {today}</h1>
"""

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