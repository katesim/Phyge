import pandas as pd
from gensim import corpora
# from DBController import DBController
from Models.PhygeArticle import BaseArticle
import numpy as np


class TrainingSample:
    LIMIT = 9000

    def __init__(self,articles):
        self.articles_id = 0
        self.articles = articles
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()

    def build_dictionary(self):
        documents = IterDict(self.articles)
        dct = corpora.Dictionary(documents)
        return dct

    def get_corpus(self): 
        return IterCorpus(my_dict=self.dictionary,my_artilces=self.articles)

    def get_documents(self):
        return IterDict(self.articles)


class IterDict:
    def __init__(self, my_articles):
        self.articles = my_articles

    def __iter__(self):
        for article in self.articles:
            yield article.normalized_words


class IterCorpus:
    def __init__(self, my_dict, my_artilces):
        self.dictionary = my_dict
        self.articles = my_artilces

    def __iter__(self):
        for article in self.articles:
            yield self.dictionary.doc2bow(article.normalized_words)

