# LIBRARIES IMPORTED
import re                           # Allows for RegEx
import requests                     # Allows for HTTP requests
from collections import defaultdict # Library to import default dict


#==============================
# Utility Function
#==============================
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
    return tag_dict[key].append(full_tag_string)

def _get_full_tag(open_tag, close_tag, html_page):
    return html_page[open_tag.start():close_tag.end()]

def _check_if_tags_match(open_tag, close_tag):
    return open_tag[1:] == close_tag[2:]

def _update_tags(tag):
    return re.sub(r'<(/?\S*)[^>]*>', r'<\1>', tag)

def _clean_tags(tag):
    return re.sub(r'</?(\S+)[^>]*>', r'\1', tag.group())

def _loop_tags(tag_iter, html_page, tag_dict):
    tag_stack   = []
    avoid_tags  = [ "meta", "link", "col"]

    for tag in tag_iter:
        clean_tag_name = _clean_tags(tag)
        if clean_tag_name in avoid_tags:
            continue

        # If the tag is a closing tag
        # compare it with the tag in the top of the stack
        if re.match(r'</[^>]*>', tag.group()):
            top_stack_tag = tag_stack[-1]              # grab the tag's object
            open_tag_name = top_stack_tag.group()
            close_tag_name = tag.group()

            # Check if the closing tag matches the open tag
            if _check_if_tags_match(_update_tags(open_tag_name),
                                    _update_tags(close_tag_name)):

                # Grab the full text from start of tag to end of tag
                full_tag_string = _get_full_tag(top_stack_tag, tag,
                                               html_page)

                # Add the tag and full text to a dictionary
                _tag_dict_items(clean_tag_name, full_tag_string, tag_dict)

                # pop item from list
                tag_stack.pop()

            else:
                tag_stack.pop()
        else:
            tag_stack.append(tag)

def tags_iterator(html_page):
    return re.finditer(r'<[^>]+>', html_page)

class REScraper:
    def __init__(self, url: str):
        self._html_page       = request_web_page(url).text
        self._tag_dict        = defaultdict(list)

        tags = tags_iterator(self._html_page)
        _loop_tags(tags, self._html_page, self._tag_dict)

    def find_all(self, tag):
        print(self._tag_dict[tag])
        return self._tag_dict[tag]
