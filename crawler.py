#!/bin/env python3

import requests as req
import requests.exceptions
import re
import sys

# Get the webpage
def get_url(url) -> str:
    r = req.get(url)

    return r.text

# Find potential webpages including "included_word"
def find_link(file, link_included_word) -> list:
    matches = re.findall('https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)', file)

    matches = [match for match in matches if link_included_word in match]

    return list(dict.fromkeys(matches))  # Remove duplicates by converting to class first

# Find potential domains/subdomain including "included_word"
def find_domain(file, domain_included_word) -> list:
    matches = re.findall('(https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256})', file)
    
    # (http[s]?:\/\/)?([^\/\s]+\/)(.*)

    matches = [match for match in matches if domain_included_word in match]

    return list(dict.fromkeys(matches))

# Find potential APIs
def find_api(file, api_included_word, api_keyword) -> list:
    matches = re.findall('https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)', file)

    matches = [match for match in matches if api_keyword in match and api_included_word in match]

    return list(dict.fromkeys(matches))

# Find potential files with the given extension (if not given, all extensions)
def find_js_files(file, js_included_word, file_extension='js') -> list:
    matches = re.findall('https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)\\.' + file_extension, file)

    matches = [match for match in matches if js_included_word in match]

    return list(dict.fromkeys(matches))

def main():
    target = sys.argv[1]
    link_included_word = ''  #TODO: Take api_included_word from user
    domain_included_word = ''  #TODO: Take domain_included_word from user
    api_included_word = ''  #TODO: Take api_included_word from user
    api_keyword = 'api'  #TODO: Take api_keyword from user
    js_included_word = ''  #TODO: Take js_included_word from user

    try:
        page = get_url(target)  #TODO: Take target from user
    except requests.exceptions.ConnectionError:
        print("The target doesn't exist.")
        sys.exit()
        
    links = find_link(page, link_included_word)
    domains = find_domain(page, domain_included_word)
    apis = find_api(page, api_included_word, api_keyword)
    files = find_js_files(page, js_included_word)

    print("\n---- LINK ----")
    for link in links:
        print(link)

    print("\n---- DOMAIN ----")
    for domain in domains:
        print(domain)

    print("\n---- API ----")
    for api in apis:
        print(api)

    print("\n---- JS ----")
    for file in files:
        print(file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a web page to crawl")
        sys.exit()

    main()

