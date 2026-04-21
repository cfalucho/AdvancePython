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


    # ==============================================================
    # Uncomment out the following statements below to test Beautiful Soup
    # Scraper
    # ==============================================================
    # soup = BS4Scraper(url)

    # === Find all table tags ===
    # key, value = soup.find_table()
    # default_dict = storage_format(key, value)
    # print(default_dict)

    # === Find all tr tags ===
    # key, value = soup.find_tr()
    # default_dict = storage_format(key, value)
    # print(default_dict)

    # === Find all th tags ===
    # key, value = soup.find_th()
    # default_dict = storage_format(key, value)
    # print(default_dict)

    # === Find all td tags ===
    # key, value = soup.find_td()
    # default_dict = storage_format(key, value)
    # print(default_dict)


if __name__ == "__main__":
    main()






