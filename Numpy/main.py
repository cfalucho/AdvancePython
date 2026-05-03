import urllib3
import requests

import pandas as pd
from REScraper import REScraper
from BS4Scraper import BS4Scraper
from DNATableModel import PandasDashboard
from DNAStrand import DNAStrand
from GUI import GUI
import numpy as np


urllib3.disable_warnings()


def request_web_page(url, timeout=10):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response

    except requests.exceptions.Timeout as err:
        print(f"Request timed out after {timeout} seconds", err)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred", err)

def open_file(file):
    try:
        if file:
            with open(file, "r", encoding="utf-8") as file_handle:
                return file_handle.read()
        return None
    except Exception as e:
        print(f"Parse error {e}")
        return None

def scrape_web_page(url):
    """
    ============= !!!  ONLY USE THIS SECTION FOR scrape_web_page !!! =============
    """
    web_scraper = REScraper(url)
    GUI(web_scraper)

def main():
    # url = ("https://mdn.github.io/learning-area/html"
    #        "/tables/assessment-finished/planets-data.html")

    html_source = "DNATable.html"


    # Open the HTML file
    o_file = open_file(html_source)



    # Pass the file to the Beautiful Soup Class to parse it
    html_scraper = BS4Scraper(o_file)


    # strands_name_arr = np.array(html_scraper.find_all("th"))
    # print(strands_name_arr)
    # dna_strands_arr = np.array(html_scraper.find_all("td"))
    # print(dna_strands_arr)
    # Pass to the Pandas Dashboard to clean up the data
    # dashboard = PandasDashboard(strands_name_arr, dna_strands_arr)


    strand_1 = "ATGTGCCTACTGTAG"
    # strand_2 = "ATG TTT ATT GGC ACT TAA"
    strand_3 = "ATGCTTCTGGTACGgGTGGTCGGGGCAACGTAA"
    # strand_39 = "ATGGGCACAGAAGGAAGAATTAATAGACCGTGA"

    codon_color_pair_list = DNAStrand(strand_1)
    # codon_color_pair_list.split_string_into_codons()


    # Display it on the Web Scraper App
    # GUI(html_scraper)



    # ==============================================================
    # Uncomment out scrape_web_page(url) to test REScraper.py
    # ==============================================================
    # html_scraper = BS4Scraper(request_web_page(url).text)
    # html_scraper.parser()
    # GUI(html_scraper)



if __name__ == "__main__":
    main()






