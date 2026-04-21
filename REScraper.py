# LIBRARIES IMPORTED
import re                           # Allows for RegEx
import requests                     # Allows for HTTP requests
from collections import defaultdict # Library to import default dict

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

def _tag_dict_items(key, full_tag_string, tag_dict):
    tag_dict[key].append(full_tag_string)
    return tag_dict

def _get_full_tag(open_tag, close_tag, html_page):
    o_start, o_end = open_tag.span()
    c_start, c_end = close_tag.span()
    return html_page[o_start:c_end]


def _check_if_tags_match(open_tag, close_tag):
    return open_tag[1:] == close_tag[2:]

def _update_tags(tag):
    tag_updated = re.sub(r'<(/?\S*)[^>]*>', r'<\1>', tag)
    return tag_updated

def _clean_tags(tag):
    return re.sub(r'</?(\S+)[^>]*>', r'\1', tag.group())

def _loop_tags(tag_iter, html_page, tag_dict):

    tag_stack = []
    avoid_tags = ["col", "meta", "link"]
    for tag in tag_iter:
        clean_tag_name = _clean_tags(tag)

        if clean_tag_name in avoid_tags:
            continue

        # print("Current Tag:", tag.group())
        if re.match(r'</[^>]*>', tag.group()):
            top_stack_tag = tag_stack[-1]
            open_tag_name = top_stack_tag.group()
            close_tag_name = tag.group()

            # check if the closing tag matches the open tag in the stack
            if _check_if_tags_match(_update_tags(open_tag_name),
                                    _update_tags(close_tag_name)):

                # Grab the full string from start of string to end of string
                full_tag_string = _get_full_tag(top_stack_tag, tag,
                                               html_page)

                # Add the full string to a dictionary
                _tag_dict_items(clean_tag_name, full_tag_string, tag_dict)

                # pop item from list
                tag_stack.pop()

            else:
                tag_stack.pop()
        else:
            tag_stack.append(tag)


class REScraper:
    def __init__(self, url: str):
        self._html_page       = request_web_page(url).text
        self._tag_dict        = defaultdict(list)

        tags_iter = re.finditer(r'<[^>]+>', self._html_page)
        _loop_tags(tags_iter, self._html_page, self._tag_dict)


    def find_all(self, tag):
        print(self._tag_dict[tag])
        return self._tag_dict[tag]
