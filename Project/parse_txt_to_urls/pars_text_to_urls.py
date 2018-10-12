from pprint import pprint
import re
import json
data = open('for_parse_url.txt', 'r', encoding="utf-8").read()


def get_links(chat_string):
    pattern = '(https?://[^\s]+)'
    return re.findall(pattern, chat_string)

links = get_links(data)

urls = []
for link in links:
    urls.append({'url': link})

pprint(urls)

with open('urls_from_file.json', 'w+', encoding='utf8') as file:
    json.dump(urls, file, indent=2)