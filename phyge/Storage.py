

import json
import os

from gensim import corpora, models

from PhygeVariables import PhyVariables
# from DBController import DBController
from TematicModels import BaseModel, LsiModel, LdaModel, D2vModel
from Models.TrainingSample import TrainingSample
from Models.PhygeArticle import BaseArticle


from BooksFetcher import BooksFetcher

class Storage:

    @classmethod
    def save_model(cls, model: BaseModel, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        if model.type is not 'd2v':
            model.dictionary.save(os.path.join(path, f'{model.name}.dict'))
            corpora.MmCorpus.serialize(os.path.join(path, f'{model.name}.mm'), model.corpus)
        model.model.save(os.path.join(path, f'{model.name}.{model.type}'))
        cls.save_articles_id(model.training_sample.articles, path)

    @classmethod
    def load_model(cls, path: str, model_name: str, model_type: str) -> BaseModel:
        print(f'{model_name}.{model_type} model loading...')
        if model_type != 'd2v':
            dictionary = corpora.Dictionary.load(os.path.join(path, f'{model_name}.dict'))
            corpus = corpora.MmCorpus(os.path.join(path, f'{model_name}.mm'))

        # articles_id = cls.load_articles_id(path)
        # articles = DBController.get_all_articles({'serial_id': {'$in': articles_id}})


        with open('Tests/test_mif/books.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
            books = json.load(fh)  # загружаем из файла данные в словарь data
        # pprint(books)

        book_fetcher = BooksFetcher(books)
        articles = book_fetcher.create_article()

        training_sample = TrainingSample(articles)

        def load_func(model_path: str, model_type: str):
            if model_type == 'lsi':
                model = models.lsimodel.LsiModel.load(model_path)
                return LsiModel.trained(name=model_name, model=model,
                                        corpus=corpus, dictionary=dictionary, training_sample=training_sample)
            elif model_type == 'lda':
                model = models.ldamodel.LdaModel.load(model_path)
                return LdaModel.trained(name=model_name, model=model,
                                        corpus=corpus, dictionary=dictionary, training_sample=training_sample)
            elif model_type == 'd2v':
                model = models.doc2vec.Doc2Vec.load(model_path)
                return D2vModel.trained(name=model_name, model=model, corpus=None, dictionary=None,
                                        training_sample=training_sample)
        model = load_func(os.path.join(path, f'{model_name}.{model_type}'), model_type=model_type)
        print('Loaded')

        return model

    @classmethod
    def save_articles_id(cls, articles, path: str):
        file_path = os.path.join(path, 'articles_id.json')
        articles_id = [obj.id for obj in articles]

        with open(file_path, 'w+', encoding='utf8') as file:
            json.dump(articles_id, file, indent=2)

    @classmethod
    def load_articles_id(cls, path: str) -> [int]:
        file_path = os.path.join(path, PhyVariables.articlesIdFileName)

        with open(file_path, 'r', encoding='utf8') as file:
            return json.load(file)
