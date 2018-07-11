import sys

from os.path import realpath, exists
from pdfx import PDFx

from re import sub

import json

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


def pdf2json(pdf_path = 'test.pdf', json_path_article = 'test_article.json', json_path_request = 'test_request.json'):
    
    if not exists(pdf_path):
        raise InputError("File doesnot exist")

    article, request = {},{}
    
    pdf = PDFx(pdf_path)
    text = pdf.get_text()
    
    # TODO decide what shall be here
    request['id'] = None
    
    url = realpath(pdf_path)
    
    article['url'] = url
    request['url'] = url
    
    title = [string for string in text.split('\n') if len(string) > 1][0]
    
    article['title'] = title
    request['title'] = title
    
    #TODO ?Надо бросать ошибки, если в тексте нету Abstract или Introduction?
    abstract = text[:text.find('Introduction')]
    article_text = text[text.find('Introduction'):]   

    article_text = sub('[0-9]','',article_text)
    article_text = sub(r'[^\w +/g]','',article_text)
    
    abstract = sub('[0-9]','',abstract)
    abstract = sub(r'[^\w +/g]','',abstract)
    
    article['text'] = article_text.replace('\n',' ')
    request['text'] = abstract.replace('\n',' ')
    
    if len(abstract)  == 0:
        raise InputError("Abstract error")
    
    if len(article_text) == 0:
        raise InputError("Article text error")

    request['summary'] = 'summary'
    
    with open(json_path_article, 'w', encoding="utf8") as file:
        s = json.dumps(article, indent=2, ensure_ascii=False)
        file.write(s)
    
    with open(json_path_request, 'w', encoding="utf8") as file:
        s = json.dumps(request, indent=2, ensure_ascii=False)
        file.write(s)


if __name__ == '__main__':
    pdf2json(pdf_path=sys.argv[1])