import uuid
import json
import os
import asyncio
from pprint import pprint

from DBController import DBController
from ArticleFetcher import ArticleFetcher
from Models.PhygeArticle import PhyPdfArticle
from TextNormalizer import TextNormalizer

from BooksFetcher import BooksFetcher
from Models.PhygeBook import PhyBook


class DatabaseSeeder:
    @classmethod
    def seed(cls):
        DBController.first_setup()
        cls.__seed_web_articles()
        # cls.__seed_pdf_articles()
        # cls.__seed_books()

    @classmethod
    def __seed_web_articles(cls):
        data_path = 'Resources/ru_slack_urls_clear.json'

        if not os.path.isfile(data_path):
            print('Resource does not exist!')
            return

        with open(data_path, 'r', encoding='utf8') as data_file:
            data = json.load(data_file)

            article_fetcher = ArticleFetcher()

            ioloop = asyncio.get_event_loop()

            sem = asyncio.Semaphore(5)

            tasks = [ioloop.create_task(article_fetcher.download_article(url['url'], sem)) for url in data]
            wait_tasks = asyncio.wait(tasks)
            ioloop.run_until_complete(wait_tasks)
            ioloop.close()

    @classmethod
    def __seed_pdf_articles(cls):
        data_path = 'Resources/pdf_articles.json'

        if not os.path.isfile(data_path):
            print('Resource does not exist!')
            return

        with open(data_path, 'r', encoding='utf8') as data_file:

            data = json.load(data_file)

            for index, article_data in enumerate(data):
                title = article_data['title']
                text = article_data['text']
                normalized_words = TextNormalizer.normalize(text)
                article = PhyPdfArticle({**article_data,
                                         'lang': 'en',
                                         'normalized_words': normalized_words})

                print(f'add {index+1} of the {len(data)} articles: {title}')

                if article is not None:
                    DBController.add_document(article, str(uuid.uuid4()))

    @classmethod
    def __seed_books(cls):

        data_path = 'phy-books/articles_books.json'

        if not os.path.isfile(data_path):
            print('Resource books does not exist! Сreation is in progress...')

            with open('phy-books/phy_books.json', 'r', encoding='utf8') as fh:  # собранные с сайта МИФ данные
                books = json.load(fh)
            book_fetcher = BooksFetcher(books[1:5])
            phy_books = book_fetcher.create_phy_book()
            books_list = []
            for obj in phy_books:
                books_list.append(obj.serialize())

            with open('phy-books/articles_books.json', 'w+',
                      encoding='utf8') as file:  # сереализованные обьекты PhyBooks
                json.dump(books_list, file, indent=2)
            print('Resource created')


        with open(data_path, 'r', encoding='utf8') as data_file:
            books = json.load(data_file)

            for index, book in enumerate(books):
                # current_book = book_fetcher.create_phy_book(book)
                phy_book = PhyBook(book)
                print(f'add {index+1} of the {len(books)} books: {phy_book.title}')
                if phy_book is not None:
                    DBController.add_document(phy_book, str(uuid.uuid4()))
