from search_combined import search_all_sources
from generate_report import generate_html_report

def main():
    results = search_all_sources()
    generate_html_report(results)

if __name__ == "__main__":
    main()