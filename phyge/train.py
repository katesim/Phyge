from DBController import DBController
from DatabaseSeeder import DatabaseSeeder
from Models.TrainingSample import TrainingSample
from TematicModels import LsiModel, LdaModel, D2vModel

from Storage import Storage

import json
from BooksFetcher import BooksFetcher


def check_db_status():
    db_len = 0
    for _ in DBController.get_all_articles():
        db_len += 1
    if db_len == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()


if __name__ == "__main__":

    with open('phy-books/phy_books.json', 'r', encoding='utf8') as fh:  # собранные с сайта МИФ данные
        books = json.load(fh)
    book_fetcher = BooksFetcher(books)
    phy_books = book_fetcher.create_phy_book()
    # print(phy_books[0].normalized_words)
    books_list = []
    for obj in phy_books:
        books_list.append(obj.serialize())

    with open('phy-books/articles_books.json', 'w+', encoding='utf8') as file:  # сереализованные обьекты PhyBooks
        json.dump(books_list, file, indent=2)

    check_db_status()

    articles = DBController.get_all_articles(limit=None)

    # testing_sample = TrainingSample(articles)

    # lsi = LsiModel(model_name='phyge')
    # lda = LdaModel(model_name='phyge')
    # d2v = D2vModel(model_name='phyge')

    # lsi.train_model(testing_sample)
    # lda.train_model(testing_sample)
    # d2v.train_model(testing_sample)

    # Storage.save_model(lsi, path='out/lsi')
    # Storage.save_model(lda, path='out/lda')
    # Storage.save_model(d2v, path='out/d2v')
