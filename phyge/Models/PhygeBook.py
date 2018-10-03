class PhyBook():
    id_key = 'serial_id'
    tema_key = 'tema'
    title_key = "title"
    source_key = "source"
    description_key = 'description'
    stikers_key = 'stikers'
    about_book_key = 'about_book'
    # help_book_key = 'help_book'
    # for_who_key = 'for_who'
    # about_author_key = 'about_author'
    excerption_key = 'excerption'
    text_key = "text"
    normalized_words_key = "normalized_words"

    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.id = obj.get(self.id_key)
        self.tema = obj.get(self.tema_key)
        self.title = obj.get(self.title_key)
        self.source = obj.get(self.source_key)
        self.description = obj.get(self.description_key)
        self.stikers = obj.get(self.stikers_key)
        self.about_book = obj.get(self.about_book_key)
        # self.help_book = obj.get(self.help_book_key)
        # self.for_who = obj.get(self.for_who_key)
        # self.about_author = obj.get(self.about_author_key)
        self.excerption = obj.get(self.excerption_key)
        self.type = 'book'
        self.text = obj.get(self.text_key)
        self.normalized_words = obj.get(self.normalized_words_key)

    def serialize(self):
        return {
            self.id_key: self.id,
            self.tema_key: self.tema,
            self.title_key: self.title,
            self.source_key: self.source,
            self.description_key: self.description,
            self.stikers_key: self.stikers,
            self.about_book_key: self.about_book,
            # self.help_book_key: self.help_book,
            # self.for_who_key: self.for_who,
            # self.about_author_key: self.about_author,
            self.excerption_key: self.excerption,
            "type": "book",
            self.text_key: self.text,
            self.normalized_words_key: self.normalized_words}

    def __str__(self):
        return self.title
