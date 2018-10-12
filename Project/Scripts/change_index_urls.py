import json
from pprint import pprint


with open('Resources/en_slack_urls_clear.json', 'r', encoding="utf8") as json_file:
    en_urls_clear = json.load(json_file)

with open('Resources/ru_slack_urls_clear.json', 'r', encoding="utf8") as json_file:
    ru_urls_clear = json.load(json_file)

all_urls = en_urls_clear + ru_urls_clear


for index, articles in enumerate(all_urls):
    articles['id'] = index
pprint(all_urls)

with open('Tests/test_6/urls.json', 'w+', encoding="utf8") as file:
    json.dump(all_urls, file, indent=2, ensure_ascii=False)
