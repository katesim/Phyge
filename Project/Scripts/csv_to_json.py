from pprint import pprint
import pandas as pd
import json

data = pd.read_csv('Tests/test_1/urls.csv')
urls = data.iloc[:, 0].tolist()
title = data.iloc[:, 1].tolist()

id = 0
result = []
for index, url in enumerate(urls):
    result.append(dict(id=id,
                       data=None,
                       title=title[index],
                       url=url,
                       chanel=None))
    id += 1

with open('Resources/urls.json', 'w+', encoding="utf8") as file:
    json.dump(result, file, indent=2, ensure_ascii=False)

pprint(result)
