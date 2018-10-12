import json
from pprint import pprint

with open('Tests/test_6/tmp/articles.json', 'r', encoding="utf8") as json_file:
    articles = json.load(json_file)

words = dict(url='', count='')
for article in articles:
    if len(article['normalized_words']) < 50:
        print('LEN ', len(article['normalized_words']), 'url', article['url'])
