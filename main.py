import urllib3
from REScraper import REScraper
from BS4Scraper import BS4Scraper
from GUI import GUI

urllib3.disable_warnings()

def scrape_web_page(url):
    """
    ============= !!!  ONLY USE THIS SECTION FOR scrape_web_page !!! =============
    """
    web_scraper = REScraper(url)
    GUI(web_scraper)


def main():
    url = ("https://mdn.github.io/learning-area/html"
           "/tables/assessment-finished/planets-data.html")

    # ==============================================================
    # Uncomment out scrape_web_page(url) to test REScraper.py
    # ==============================================================
    scrape_web_page(url)


if __name__ == "__main__":
    main()






