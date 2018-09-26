# -*- coding: utf-8 -*-

import requests
from lxml import html
from pprint import pprint
import json


# список книг с главной страницы
def create_list_books(main_page_url='https://www.mann-ivanov-ferber.ru/books/allbooks/'):
    # url = 'https://www.mann-ivanov-ferber.ru/books/allbooks/'  # % (user_id) # url для второй страницы
    r = requests.get(main_page_url)
    tree = html.fromstring(r.text)
    books_list_lxml = tree.xpath('//div[@class = "c-continuous-list"]/div/a[@class = "c-book p-img-block"]/@href')
    return books_list_lxml


def create_book_json(url='https://www.mann-ivanov-ferber.ru/books/mashina-pravdyi/'):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    books = dict()
    books["tema"] = '. '.join(list(set(tree.xpath('//div[@class = "nkk-book-tags__wrapper js-wrapper"]'
                                                  '/a[@class="nkk-book-tags-item js-item"]/span/text()'))))
    books['title'] = tree.xpath('//h1[@class = "header active p-sky-title"]/span/text()')[0]
    books['source'] = url
    try:
        books['description'] = tree.xpath('//p[@class = "body active"]/text()')[0]
    except:
        books['description'] = ''
    books['stikers'] = '. '.join(tree.xpath('//span/span[@class = "wrap"]/text()')).replace("\xa0", ' ')
    books['about_book'] = ' '.join(tree.xpath('//section[@class="l-about-book b-about-book"]/div/div[@class '
                                              '= "description"]/div/p/text()')).replace("\xa0", ' ')
    books['excerption'] = ' '.join(tree.xpath('//div[@class="border slider-pane"]/div'
                                              '/div[@class = "item slider-item"]/div/p/text()')).replace("\xa0", ' ')
    img = 'https://www.mann-ivanov-ferber.ru/' + tree.xpath('//div[@class="img-wrapper"]/img/@src')[0]
    p = requests.get(img)
    with open('./img/' + str(books['title']) + '.png', "wb") as file:
        file.write(p.content)

    return books


# список ссылок на книжки с главной страницы
books_list_lxml = create_list_books()
print(books_list_lxml)
# with open('books_list_lxml.json', 'w+', encoding='utf8') as file:
#     json.dump(books_list_lxml, file, indent=2)

books = []
for url in books_list_lxml:
    print(url)
    book = create_book_json(url)
    books.append(book)
pprint(books)

with open('phy_books.json', 'w+') as file:
    json.dump(books, file, indent=2)
#
# books = create_book_json()
# print(books)
