from Models.Query import BaseQuery

from TematicModels import BaseModel


class SearchEngine:
    def __init__(self, models: [BaseModel]):
        self.models = models

    def find_article(self, query: BaseQuery, amount=5):
        search_results = dict()
        for model in self.models:
            similarities = model.perform_search(normalized_query=query.normalized_words)
            articles = model.training_sample.articles
            found_articles = list()

            for index, similarity in similarities[:amount]:
                answer = {'id': articles[index].id,
                          'title': articles[index].title,
                          'source': articles[index].source,
                          'text': (articles[index].text[0:200])\
                                      .replace("', '", '')\
                                      .replace("[, ", '')\
                                      .replace("'", '')\
                                      .replace(", ,", '')\
                                      .replace("[", '')\
                                  + '...',
                          'similarity': round(float(similarity), 3)}
                found_articles.append(answer)
            search_results[model.type] = found_articles

        return search_results


if __name__ == '__main__':
    pass
