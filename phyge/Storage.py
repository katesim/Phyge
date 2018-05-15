import pandas as pd
import json
import os

from ArticleSerializer import ArticleSerializer

from Models.PhygeVariables import PhyVariables
from Models.TestCase import TestCase
from Models.Query import Query


class Storage:

    def load_test_case(self, test_case_id):
        test_case_path = str.format('{0}/test_{1}', PhyVariables.testsPath, test_case_id)
        data_url = pd.read_csv(test_case_path + '/' + PhyVariables.urlsFileKey)
        urls = data_url.iloc[:, 0]
        queries = self.__load_queries(test_case_path + '/' + PhyVariables.queriesFileKey)

        saved_articles, values = list(), None

        if os.path.isfile(test_case_path + '/' + PhyVariables.articlesFileKey):
            saved_articles = ArticleSerializer.deserialize(test_case_path + '/' + PhyVariables.articlesFileKey)

        if os.path.isfile(test_case_path + '/' + PhyVariables.valuesFileKey):
            values = pd.read_csv(test_case_path + '/' + PhyVariables.valuesFileKey)

        return TestCase(test_case_id, {'urls': urls,
                                       'path': test_case_path,
                                       'queries': queries,
                                       'articles': saved_articles,
                                       'values': values})

    def __load_queries(self, queries_json_path) -> [Query]:
        if not os.path.isfile(queries_json_path):
            return list()

        with open(queries_json_path, 'r') as file:
            queries = json.load(file)
            return [Query(obj) for obj in queries]