import re as re
from googletrans import Translator
from math import ceil

SYMBOL_LIMIT = 5000


class PhyTranslate:
    def __init__(self):
        print('Translate')

    @classmethod
    def detect_language(self, text):
        try:
            return Translator().detect(text[:SYMBOL_LIMIT]).lang # Смотрим на первые 5000 символов, чтобы не было переполнения у гугловского сервера
        except:
            print('Error while detecting')
            return ''

    @classmethod
    def translate(self, text, title, downloaded_from_url):
        try:
            if len(text) < SYMBOL_LIMIT:
                return Translator().translate(text, dest='ru').text
            else:
                block_number = ceil(len(text) / SYMBOL_LIMIT)
                translated_text = ''
                for i in range(block_number):
                    translated_text += Translator().translate(text[SYMBOL_LIMIT * i:SYMBOL_LIMIT * (i + 1)],
                                                              dest='ru').text
                return translated_text
        except:
            print('Error while translating')
            with open('out_info.txt', 'a') as info:
                info.write(
                    "Cann't be translated " + re.sub(r'[^\x00-\x7f]', '', title) + " " + downloaded_from_url + "\n")
            return text
