import re
import pymorphy2


class TextNormalizer:

    @classmethod
    def normalize(cls, text):
        text_tokens = cls.__tokenize_text(text)
        # russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
        # russian_words = cls.__normalize_tokens(russian_words)
        russian_words = cls.__normalize_tokens(text_tokens)
        stopwords = cls.stopwords()
        return list(filter(lambda x: x not in stopwords and len(x) > 1, russian_words))

    @classmethod
    def __tokenize_text(cls, text):
        tokens = re.sub('[^\w]', ' ', text).split()
        return list(map(str.lower, tokens))

    @classmethod
    def __normalize_tokens(cls, tokens):
        morph = pymorphy2.MorphAnalyzer()
        return list(map(lambda x: morph.parse(x)[0].normal_form, tokens))

    @classmethod
    def stopwords(cls):
        with open('Resources/stopwords/russian_english', 'r', encoding='utf8') as file:
            lines = file.readlines()
            return [line.replace('\n', '') for line in lines]
