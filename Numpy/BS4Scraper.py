import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict # Library to import default dict


#==============================
# Utility Function
#==============================
def remove_whitespace(text):
    clean_text = text.strip("\n")
    return clean_text

class BS4Scraper:
    def __init__(self, html):
        self._soup         = BeautifulSoup(html,"html.parser")
        self.tag_dict      = defaultdict(list)


        # remove thead Sample DNA Table
        self._soup.thead.decompose()

        # for tags that are parents
        for tag in self._soup.find_all(True):
            for strings in tag.stripped_strings:
                self.tag_dict_items(tag.name, strings)

    def find_all(self, tag):
        return self.tag_dict[tag]

    def tag_dict_items(self, key, string_text):
        return self.tag_dict[key].append(string_text)

    def display_dict(self, tag):
        for tag, value in self.tag_dict.items():
            print(f"{tag}: {value}", end="\n\n")

    def get_items(self):
        return self.tag_dict








