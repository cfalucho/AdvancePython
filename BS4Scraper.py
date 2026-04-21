import requests
from bs4 import BeautifulSoup

#==============================
# Utility Function
#==============================
def request_web_page(url, timeout=10):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response

    except requests.exceptions.Timeout as err:
        print(f"Request timed out after {timeout} seconds", err)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred", err)

class BS4Scraper:
    def __init__(self, url):
        self._url = url
        self._soup = BeautifulSoup(request_web_page(url).text,
                                   "html.parser")


    def find_table(self):
        table = self._soup.table
        key = table.name

        # If table is none, return none
        if table is None:
            return None

        value = table.contents
        return key, value


    def find_tr(self):
        tr = self._soup.tr
        key = tr.name

        # If tr is none, return none
        if tr is None:
            return None

        value = tr.contents

        return key, value


    def find_th(self):
        th = self._soup.th
        key = th.name
        value = ""

        # If th is none, return none
        if th is None:
            return None

        # Check if tag has a parent or children
        has_parent = th.parent
        has_children = len(th.contents) > 0

        if has_parent or has_children:
            value = self._soup.find_all(key)


        return key, value


    def find_td(self):
        td = self._soup.td
        key = td.name
        value = ""

        # If td is none, return none
        if td is None:
            return None

        # Check if tag has a parent or children
        has_parent = td.parent
        has_children = len(td.contents) > 0

        if has_parent or has_children:
            value = self._soup.find_all(key)


        return key, value









