from Models.BagOfWordsModel import BagOfWordsModel

from TextNormalizer import TextNormalizer


class BaseQuery(object):
    idKey = 'id'
    textKey = 'text'
    sourceKey = 'url'

    def __init__(self, obj: dict):
        self.id = obj.get(self.idKey, None)
        self.text = obj.get(self.textKey, None)
        self.source = obj.get(self.sourceKey, None)

    def __str__(self):
        return ' '.join(self.normalized_words)

    def uci_representation(self, path):
        bag_of_words = BagOfWordsModel({self.id: self.text})
        bag_of_words.to_uci(model_name='query', save_folder=path + '/uci')

    @property
    def normalized_words(self) -> [str]:
        return TextNormalizer.normalize(self.text)
