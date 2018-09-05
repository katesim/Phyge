import pandas as pd
from gensim import corpora
from DBController import DBController
from Models.PhygeArticle import BaseArticle


class TrainingSample:
    #LIMIT = 10

    def __init__(self,articles):
        self.articles_id = self.get_articles_id(articles)
        self.articles = self.get_articles()
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()
    
    def get_articles_id(self,articles):
        articles_id = []
        for article in articles:
            articles_id.append(article['serial_id'])
        return articles_id

    def get_articles(self):
        return IterArticles(self.articles_id)

    def build_dictionary(self):
        documents = IterDict(self.articles)
        dct = corpora.Dictionary(documents)
        return dct

    def get_corpus(self): 
        return IterCorpus(my_dict=self.dictionary,my_artilces=self.articles)

    def get_documents(self):
        return IterDict(self.articles)


class IterArticles:
    def __init__(self,articles_id):
        self.articles_id = articles_id
    
    def __len__(self):
        return len(self.articles_id)
    
    def __getitem__(self,key):
        if isinstance(key,slice):
            return [BaseArticle(DBController.get_article(self.articles_id[ii])) 
                for ii in range(*key.indices(len(self)))]
        elif isinstance(key,int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("The index {} is out of range.".format(key))
            return BaseArticle(DBController.get_article(self.articles_id[key])) 
        else:
            raise TypeError("Invalid argument type.")

    def __iter__(self):
        for id in self.articles_id:
            yield BaseArticle(DBController.get_article(id))

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

