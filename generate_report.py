from datetime import date
import os

def generate_html_report(results):
    today = date.today().isoformat()
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Raport {today}</title></head><body>
<h1>Raport dzienny – {today}</h1><ol>"""
    for r in results:
        html += f"<li><a href='{r['url']}'>{r['title']}</a> – źródło: {r['source']}</li>"
    html += "</ol></body></html>"
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{today}.html", "w", encoding="utf-8") as f:
        f.write(html)