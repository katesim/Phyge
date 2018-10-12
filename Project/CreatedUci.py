from BagOfWordsModel import BagOfWordsModel
from CreateSearchQuery import CreateSearchQuery


class CreatedUci:
    def __init__(self, text_query='', article='', save_folder='tests'):
        # CREATE UCI
        self.save_folder = save_folder
        self.text_query = {'test_text': str(text_query)}
        self.article = article
        self.text_article = self.create_dict_article_for_uci()

    def create_dict_article_for_uci(self):
        dict_kek = {}
        for i in range(0, len(self.article)):
            dict_kek.update({i: str(self.article[i].normalized_words)})
        return dict_kek

    def create_uci(self, text=dict, model_name=str):
        bag_of_words = BagOfWordsModel(text)
        bag_of_words.to_uci(model_name=model_name, save_folder=self.save_folder)
        print('OK Create uci from', model_name, '(to', self.save_folder, ')')


if __name__ == '__main__':
    text_query = CreateSearchQuery().text_normalize
    create_uci = CreatedUci(text_query=text_query)
