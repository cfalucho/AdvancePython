import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict # Library to import default dict


#==============================
# Utility Function


def remove_whitespace(text):
    clean_text = text.strip("\n")
    return clean_text


class BS4Scraper:
    def __init__(self, html):
        self._soup         = BeautifulSoup(html,"html.parser")
        self.tag_dict      = defaultdict(list)


    def parser(self):
        # remove thead Sample DNA Table
        self._soup.thead.decompose()

        # if tag is a parent
        for tag in self._soup.find_all(True):
            for strings in tag.stripped_strings:
                self.tag_dict_items(tag.name, strings)

            # print("parent:", remove_whitespace(tag.name))
            # if tag.contents:
            #     # print("This tag is a children", tag.name)
            #     for child in tag.descendants:
            #         print("child:", child)
            # for element in tag:
            #     print(element)
            # self.tag_dict_items(tag.name, remove_whitespace(tag.text))

    # def find_multiple_tags(self, *multi_tags):
    #
    #     tags = self._soup.find_all(multi_tags)
    #
    #     if not tags:
    #         print("Tag not found.")
    #         return
    #     for tag in tags:
    #         for element in tag:
    #             self.tag_dict_items(tag, f"{element.text}")
    #             # print(f"{element.text}")


    def find_all(self, tag):
        print(self.tag_dict[tag])
        return self.tag_dict[tag]

    def tag_dict_items(self, key, string_text):
        return self.tag_dict[key].append(string_text)

    def display_dict(self, tag):

        for tag,value in self.tag_dict:
            print(f"{tag}: {value}", end="\n\n")








