import urllib3
import requests

from REScraper import REScraper
from BS4Scraper import BS4Scraper
from DNAStrand import DNAStrand
from DNATableModel import DNATableModel
from DNAViewerGUI import DNAViewerGUI
from Strand import Strand
import pandas as pd

from GUI import GUI

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

def open_file(file_path):
    try:
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file_handle:
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
    html_file = "DnaRna_Table.html"

    # Open the HTML file
    o_file = open_file(html_file)

    # Pass the file to the Beautiful Soup Class to parse it
    html_scraper = BS4Scraper(o_file)

    strands_name_arr = html_scraper.find_all("th")
    # print(strands_name_arr)
    dna_strands_arr = html_scraper.find_all("td")
    # print(dna_strands_arr)

    # pass to the Pandas Dashboard to clean up the data
    # pandas_series = DNATableModel(strands_name_arr, dna_strands_arr)
    series_from_lists = pd.Series(dna_strands_arr)

    # dna_objects_series = series_from_lists.apply(Strand)
    Strand("CACAZU#9GXG1TGAXACA")


    #
    #  pass to DNAViewerGUI
    # DNAViewerGUI(pandas_series)


    """
        ============= !!!  TESTING PURPOSES !!! =============
    """
    strand_1 = "ATGTGCCTACTGTAG"
    strand_2 = "ATG TTT ATT GGC ACT TAA"
    strand_3 = "AATCTAATTGGCACTTGA"
    strand_4 = "ATGCTTCTGGTACGbGTGGTCGGGGCAACGTAA"
    strand_39 = "ATGGGCACAGAAGGAAGAATTAATAGACCGTGA"
    strand_86 = "ATGATCCATAGACGTTTCTTGCGTAGAACG"
    segment_1 = "AUGCUAACUUCUAUACUAGUAUGGGAUUCGUGG"
    segment_2 = "0e#aO#F!U"
    segment_3 = "ATGGGACGCGTGGCATCTAATTGA"
    segment_12 = "CZAA9TAATX1#A9"
    segment_13 = "9@AGC#GATTU@XUZAX"
    segment_14 = "@1X CCX G#U CC# CA1 @AC CTC"


    # Strand(dna_strands_arr)


    # DNAViewerGUI(result)



    # ==============================================================
    # Uncomment out scrape_web_page(url) to test REScraper.py
    # ==============================================================
    # html_scraper = BS4Scraper(request_web_page(url).text)
    # html_scraper.parser()
    # GUI(html_scraper)


if __name__ == "__main__":
    main()






