

class BaseArticle(object):
    id_key = 'serial_id'
    title_key = 'title'
    text_key = 'text'
    type_key = 'type'
    source_key = 'source'
    language_key = 'lang'
    normalized_words_key = 'normalized_words'

    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.id = obj.get(self.id_key)
        self.title = obj.get(self.title_key)
        self.text = obj.get(self.text_key)
        self.type = obj.get(self.type_key, '')
        self.source = obj.get(self.source_key, 'Unknown')
        self.language = obj.get(self.language_key, '')
        self.normalized_words = obj.get(self.normalized_words_key, list())

    def serialize(self) -> dict:
        """Serialize document"""
        return {
            self.id_key: self.id,
            self.title_key: self.title,
            self.text_key: self.text,
            self.type_key: self.type,
            self.source_key: self.source,
            self.language_key: self.language,
            self.normalized_words_key: self.normalized_words
        }

    def __str__(self):
        return self.title


class PhyWebArticle(BaseArticle):

    def __init__(self, obj=None):
        BaseArticle.__init__(self, obj)
        self.type = 'web_article'


class PhyPdfArticle(BaseArticle):
    abstract_key = 'abstract'

    def __init__(self, obj=None):
        BaseArticle.__init__(self, obj)

        if obj is None:
            obj = dict()

        self.abstract = obj.get(self.abstract_key)
        self.type = 'pdf_article'

    def serialize(self):
        base_data = super(PhyPdfArticle, self).serialize()
        return {**base_data, self.abstract_key: self.abstract}

    def __str__(self):
        return self.title
