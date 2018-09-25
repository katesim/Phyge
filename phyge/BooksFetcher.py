from TextNormalizer import TextNormalizer
from bs4 import BeautifulSoup
from pprint import pprint
from Models.PhygeArticle import PhyWebArticle
import re

import uuid

import sys
import json


class BooksFetcher:
    def __init__(self, books: list):
        self.books = books

    def create_article(self):
        article = []
        for book in self.books:
            text = book['description'] + book['stikers']
            article.append(  self.parse_books(book, text) )
        return article

    def parse_books(self, book, current_text):
        books_text = current_text
        text = self.__transform_to_single_line(books_text)
        text = re.sub(r'\{[^*]*\}', '', text)

        normalized_words = TextNormalizer.normalize(text)

        books = PhyWebArticle({
            PhyWebArticle.source_key: book['source'],
            PhyWebArticle.title_key: book['title'],
            PhyWebArticle.text_key: text,
            PhyWebArticle.language_key: '',
            PhyWebArticle.normalized_words_key: normalized_words
        })

        return books

    @staticmethod
    def __transform_to_single_line(raw_html):
        soup = BeautifulSoup(raw_html, 'lxml')
        result = str(soup.findAll(text=True)) \
            .replace("\\n", ' ') \
            .replace("\\r", ' ') \
            .replace('\\xa0', ' ') \
            .replace('\'', ' ') \
            .replace('\\t', ' ')

        return result


if __name__ == '__main__':
    with open('Tests/test_mif/phy_books.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
        books = json.load(fh)  # загружаем из файла данные в словарь data
    # pprint(books)

    book_fetcher = BooksFetcher(books)
    article = book_fetcher.create_article()
    print(article[0].normalized_words)


