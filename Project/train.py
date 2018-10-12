from DBController import DBController
from DatabaseSeeder import DatabaseSeeder
from Models.TrainingSample import TrainingSample
from TematicModels import LsiModel, LdaModel, D2vModel, FastTextModel

from Storage import Storage


def check_db_status():
    db_len = 0
    for _ in DBController.get_all_articles():
        db_len += 1
    if db_len == 0:
        print('Seeding database...')
        DatabaseSeeder.seed()


if __name__ == "__main__":
    check_db_status()

    articles = DBController.get_all_articles(limit=None)

    testing_sample = TrainingSample(articles)

    lsi = LsiModel(model_name='phyge')
    #lda = LdaModel(model_name='phyge')
    #d2v = D2vModel(model_name='phyge')
    #fast_text = FastTextModel(model_name='phyge')

    lsi.train_model(testing_sample)
    #lda.train_model(testing_sample)
    #d2v.train_model(testing_sample)
    #fast_text.train_model(testing_sample)

    Storage.save_model(lsi, path='out/lsi')
    #Storage.save_model(lda, path='out/lda')
    #Storage.save_model(d2v, path='out/d2v')
    #Storage.save_model(fast_text, path='out/fast_text')