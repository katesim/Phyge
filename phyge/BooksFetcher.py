from TextNormalizer import TextNormalizer
from bs4 import BeautifulSoup
from pprint import pprint
from Models.PhygeBook import PhyBook
import re
import requests
from lxml import html
import json
import uuid

import sys


class BooksFetcher:
    def __init__(self, books: list):
        self.books = books

    def create_phy_book(self):
        phy_books = []
        for book in self.books:
            phy_books.append(self.parse_book(book))
        return phy_books

    def parse_book(self, book):
        books_text = book['description'] + '. ' + book['stikers'] + '. ' + book["about_book"] + '. ' + \
                     book["excerption"] + '. ' + book["title"]
        text = self.__transform_to_single_line(books_text)
        text = re.sub(r'\{[^*]*\}', '', text)

        normalized_words = TextNormalizer.normalize(text)

        phy_book = PhyBook({
            # TODO сделать id
            PhyBook.id_key: 0,
            PhyBook.tema_key: book["tema"],
            PhyBook.title_key: book['title'],
            PhyBook.source_key: book['source'],
            PhyBook.description_key: book['description'],
            PhyBook.stikers_key: book['stikers'],
            PhyBook.about_book_key: book['about_book'],
            # PhyBook.help_book_key: book['help_book'],
            # PhyBook.for_who_key: book['for_who'],
            # PhyBook.about_author_key: book['about_author'],
            PhyBook.excerption_key: book['excerption'],
            "type": "book",
            PhyBook.text_key: books_text,
            PhyBook.normalized_words_key: normalized_words})
        return phy_book

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
    with open('phy-books/phy_books.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
        books = json.load(fh)  # загружаем из файла данные в словарь data
    # pprint(books)

    book_fetcher = BooksFetcher(books[1:3])
    phy_books = book_fetcher.create_phy_book()
    print(phy_books[0].normalized_words)
