from search_duckduckgo import search_duckduckgo
from generate_report import generate_html_report

def main():
    results = search_duckduckgo()
    generate_html_report(results)

if __name__ == "__main__":
    main()