import time
import abc
import os
from gensim import models, similarities

from Models.TrainingSample import TrainingSample


class BaseModel(object):
    TOPIC_NUMBER = 300
    SHARD_SIZE = 500

    @classmethod
    def trained(cls, name, model, corpus, dictionary, training_sample: TrainingSample):
        instance = cls(name)

        instance.model = model
        instance.corpus = corpus
        instance.dictionary = dictionary

        instance.training_sample = training_sample

        return instance

    def __init__(self, name, model_type):
        self.name = name
        self.type = model_type

        self.model = None
        self.training_sample = None
        self.dictionary = None
        self.corpus = None

    @abc.abstractmethod
    def train_model(self, training_sample: TrainingSample):
        """Train model."""

    def perform_search(self, normalized_query: [str]):
        if self.type == 'd2v':
            query_vec = self.model.infer_vector(normalized_query)
            sims = self.model.docvecs.most_similar([query_vec])
        else:
            index = similarities.Similarity(output_prefix=os.path.join('out', self.type, 'index_shard'),
                                            corpus=self.model[self.corpus],
                                            shardsize=self.SHARD_SIZE,
                                            num_features=self.dictionary.num_pos)

            query_vec = self.query_to_vec(normalized_query)
            query = self.model[query_vec]
            sims = index[query]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])

        return sims

    def query_to_vec(self, normalized_query: [str]):
        return self.dictionary.doc2bow(normalized_query)


class LsiModel(BaseModel):
    def __init__(self, model_name: str):
        BaseModel.__init__(self, name=model_name, model_type='lsi')

    def train_model(self, training_sample: TrainingSample):
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        self.model = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')


class LdaModel(BaseModel):
    def __init__(self, model_name: str):
        BaseModel.__init__(self, name=model_name, model_type='lda')

    def train_model(self, training_sample: TrainingSample):
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        self.model = models.ldamodel.LdaModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER,
                                              passes=20)
        print('Learning time:', round((time.time() - start_time), 3), 's')


class D2vModel(BaseModel):
    def __init__(self, model_name: str):
        BaseModel.__init__(self, name=model_name, model_type='d2v')

    def train_model(self,training_sample: TrainingSample):
        max_epochs = 100
        vec_size = 30
        alpha = 0.025
        self.training_sample = training_sample
        self.documents = training_sample.get_documents() #Разобраться с articles в классе TrainingSample
        tagged_data = [models.doc2vec.TaggedDocument(words=_d, tags=[str(i)]) for i, _d in enumerate(self.documents)]
        self.model = models.doc2vec.Doc2Vec(size=vec_size,
                        alpha=alpha,
                        #window=3,
                        min_alpha=0.00025,
                        negative=5,
                        min_count=1,
                        seed=12345,
                        dm =1)
        self.model.build_vocab(tagged_data)
        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            self.model.train(tagged_data,
                        total_examples=self.model.corpus_count,
                        epochs=self.model.epochs)
            # decrease the learning rate
            self.model.alpha -= 0.0002
            # fix the learning rate, no decay
            self.model.min_alpha = self.model.alpha

if __name__ == '__main__':
    pass
