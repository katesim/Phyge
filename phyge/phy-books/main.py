# -*- coding: utf-8 -*-

import requests
from lxml import html
from pprint import pprint
import json
import re


# список книг с главной страницы
def create_list_books():
    list_urls_books = []
    all_books_html = []
    for page in range(1, 100 + 1):
        print(page)
        main_page_url = 'https://www.mann-ivanov-ferber.ru/book/all.ajax?booktype=paperbook&page=' + str(page)
        r = requests.get(main_page_url)
        tree = json.loads(r.text, encoding='utf-8')
        all_books_html.append(tree['html'])
    list_urls_books.append(re.findall(r'https://[^"]+', ' '.join(all_books_html)))
    return list_urls_books[0]


def create_book_json(url='https://www.mann-ivanov-ferber.ru/books/mashina-pravdyi/'):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    books = dict()
    books["help_book"] = ""
    books["for_who"] = ""
    books["about_author"] = ""
    try:
        books["tema"] = '. '.join(list(set(tree.xpath('//div[@class = "nkk-book-tags__wrapper js-wrapper"]'
                                                      '/a[@class="nkk-book-tags-item js-item"]/span/text()'))))
    except:
        books["tema"] = ''

    try:
        books['title'] = tree.xpath('//h1[@class = "header active p-sky-title"]/span/text()')[0]
    except:
        books['title'] = ''

    books['source'] = url

    try:
        books['description'] = tree.xpath('//p[@class = "body active"]/text()')[0]
    except:
        books['description'] = ''

    try:
        books['stikers'] = '. '.join(tree.xpath('//span/span[@class = "wrap"]/text()')).replace("\xa0", ' ')
    except:
        books['stikers'] = ''

    try:
        books['about_book'] = ' '.join(tree.xpath('//section[@class="l-about-book b-about-book"]/div/div[@class '
                                                  '= "description"]/div/p/text()')).replace("\xa0", ' ')
    except:
        books['about_book'] = ''

    try:
        books['excerption'] = ' '.join(tree.xpath('//div[@class="border slider-pane"]/div'
                                                  '/div[@class = "item slider-item"]/div/p/text()')).replace("\xa0",
                                                                                                             ' ')
    except:
        books['excerption'] = ""

    try:
        img = 'https://www.mann-ivanov-ferber.ru/' + tree.xpath('//div[@class="img-wrapper"]/img/@src')[0]
        p = requests.get(img)
        with open('./img/' + str(books['title']) + '.png', "wb") as file:
            file.write(p.content)
    except:
        pass

    return books


# список ссылок на книжки с главной страницы
# list_urls_books = create_list_books()
# print(list_urls_books)
# with open('list_urls_books.json', 'w+') as file:
#     json.dump(list_urls_books, file, indent=2)

with open('list_urls_books.json', 'r', encoding='utf-8') as fh:
    list_urls_books = json.load(fh)

books = []
for url in list_urls_books:
    print(url)
    book = create_book_json(url)
    books.append(book)
pprint(books)

with open('phy_books.json', 'w+') as file:
    json.dump(books, file, indent=2)
