from newspaper import Article
from TextNormalizer import TextNormalizer
from readability.readability import Document
from bs4 import BeautifulSoup

from Models.PhygeTranslate import PhyTranslate
from Models.PhygeArticle import PhyWebArticle
import re

import uuid
from DBController import DBController

import aiohttp
import async_timeout
import sys


class ArticleFetcher:
    def __init__(self):
        self.word_limit = 30
        self.number_of_downloads = 0

    async def download_article(self, url: str, sem) -> PhyWebArticle:
        async with sem:
            article_html = await self.load_html(url)
            if len(article_html) > 0:
                article = self.parse_html(url, article_html)
                if len(article.normalized_words) == 0:
                    print(f'url {url} PARSE ERR')
                    article = None
            else:
                article = None

            if article is not None:
                DBController.add_document(article, str(uuid.uuid4()))


    async def load_html(self, url):
        article_html = Article(url=url, language='ru')
        html = await self.session_get_html(url)
        article_html.set_html(html)
        return article_html.html

    async def session_get_html(self, url):

        async with aiohttp.ClientSession() as session:
            return await self.__get_html(session, url)

    async def __get_html(self, session, url):
        with async_timeout.timeout(15):
            try:
                async with session.get(url) as response:
                    self.number_of_downloads += 1
                    print(f'Download {self.number_of_downloads}. Url {url}')
                    return await response.text()
            except:
                e = sys.exc_info()[0]
                file = open('file.txt', 'a')
                file.write('{\'url\': \'' + url + '\'}, \n')
                file.close()
                print(f'For url: {url} - ERROR', e)

    def parse_html(self, current_url, article_html, language='ru'):
        readable_html = Document(article_html).summary()
        title = Document(article_html).short_title()
        text = self.__transform_to_single_line(readable_html)
        text = re.sub(r'\{[^*]*\}', '', text)

        if language == 'en':
            text = PhyTranslate.translate(text, title, current_url)

        normalized_words = TextNormalizer.normalize(text)
        web_article = PhyWebArticle({
            PhyWebArticle.source_key: current_url,
            PhyWebArticle.title_key: title,
            PhyWebArticle.text_key: text,
            PhyWebArticle.language_key: language,
            PhyWebArticle.normalized_words_key: normalized_words
        })

        return web_article

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
