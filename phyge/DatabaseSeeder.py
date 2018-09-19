import uuid
import json
import os
import asyncio

from DBController import DBController
from ArticleFetcher import ArticleFetcher
from Models.PhygeArticle import PhyPdfArticle
from TextNormalizer import TextNormalizer


class DatabaseSeeder:
    @classmethod
    def seed(cls):
        DBController.first_setup()
        cls.__seed_web_articles()
        #cls.__seed_pdf_articles()

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
