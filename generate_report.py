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

def generate_html_report(results):
    today = date.today().isoformat()

    for r in results:
        r["domain"] = extract_domain(r["url"])
        r["published"] = r.get("published", "")
        r["published_source"] = r.get("published_source", "none")

    sorted_results = sorted(results, key=lambda x: (x["domain"], x["published"]))

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Raport {today}</title></head><body>
<h1>Raport dzienny – {today}</h1><ol>"""

    for r in sorted_results:
        translated = translate_to_polish(r['title'])
        timestamp = r['published'] if r['published'] else "brak danych"
        origin = r['published_source'] if r['published_source'] != "none" else "nieznana"
        html += f"<li><a href='{r['url']}'>{r['title']}</a><br>"
        html += f"<i>{translated}</i><br>"
        html += f"<b>Źródło:</b> {r['domain']} &nbsp;&nbsp; "
        html += f"<b>Data publikacji:</b> {timestamp} "
        html += f"(<i>{origin}</i>)</li>"

    html += "</ol></body></html>"
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{today}.html", "w", encoding="utf-8") as f:
        f.write(html)