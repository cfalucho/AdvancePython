# LIBRARIES IMPORTED
import re                           # Allows for RegEx
import requests                     # Allows for HTTP requests
from collections import defaultdict # Library to import default dict


def _construct_open_tag(tag: str):
    """Constructs open tag"""
    open_tag = "<" + tag
    return open_tag

def request_web_page(url: str, timeout=10):
    try:
        # Test this block of code for errors, when making a request
        response = requests.get(url, timeout=timeout, verify=False)
        response.raise_for_status()
        return response

    except requests.exceptions.Timeout as err:
        print(f"Request timed out after {timeout} seconds", err)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred", err)


class REScraper:
    def __init__(self, url: str):
        self._html_page       = request_web_page(url).text
        self.dict_items = defaultdict(str)


    def get_user_input(self, user_input=None):
        user_input = input("Enter a tag: ")

        return user_input, self.find_all(user_input)

    def find_all(self, tag):
        remove_tag = tag.strip("<>")
        tag_list = []
        element_found = self._is_element_found(remove_tag)
        pattern_tag = fr'<{remove_tag}[\s\S]*?[\s\S]*?</{remove_tag}>'

        if element_found:
            for word in re.findall(pattern_tag, self._html_page):
                tag_list.append(word)
        else:
            return f"{tag} not found."


        combine_string = "".join(tag_list)
        return combine_string

    def _is_element_found(self, tag):
        # construct the tag
        tag_constructed = _construct_open_tag(tag)
        # check if the tag exists in the string
        if tag_constructed in self._html_page:
            return True
        else:
            return False


    def get_dict_items(self):
        return self.dict_items


    def storage_format(self, key: str, value: str):
        """
        Pass in a key str and value str, then create a default dict

        :return: a default dictionary
        """
        self.dict_items[key] = value


        return self.dict_items