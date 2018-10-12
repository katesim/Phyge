import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import logging


class BagOfWordsModel(object):
    OUT_FOLDER = 'out'

    def __init__(self, id_document_dict, max_features=None, max_df=1.0):
        """Builds bow model.

        Args:
            id_document_dict: ids of documents and theirs contents in format
                "{id: 'text', ...}"
            max_features: If not None, build a vocabulary that only consider the top
                max_features ordered by term frequency across the corpus.
                This parameter is ignored if vocabulary is not None.
            max_df: When building the vocabulary ignore terms that have a
                document frequency strictly higher than the given threshold
                (corpus-specific stop words). If float, the parameter
                represents a proportion of documents, integer absolute counts.
                This parameter is ignored if vocabulary is not None.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Building bag-of-words model with max_features={0}, max_df={1}".format(
                max_features, max_df))
        self.logger.info("Size of data set: " + str(len(id_document_dict)))

        if len(id_document_dict) != 0:
            self.logger.info("Building pandas dataframe")
            df = pd.DataFrame.from_dict(data=id_document_dict, orient='index')
            self.logger.info("Built pandas dataframe")
            ids = df.index
            self.index2id = dict(enumerate(ids))
            self.id2index = {v: k for k, v in self.index2id.items()}
            documents_corpus = df[0].values  # 1-dim np.array.
            # documents_corpus = documents_corpus.astype(unicode)
            del df
            if max_features is None:
                self.logger.info(
                    "Training CountVectorizer with all {0} features".format(
                        len(ids)))
            else:
                self.logger.info(
                    "Training CountVectorizer with max {0} features".format(
                        max_features))
            vectorizer = CountVectorizer(max_features=max_features,
                                         max_df=max_df,
                                         stop_words='english').fit(
                documents_corpus)
            self.logger.info("Trained vectorizer with {0} features".format(
                len(vectorizer.get_feature_names())))
            self.logger.info("Building bag-of-words model")
            bow = vectorizer.transform(documents_corpus)
            self.logger.info("Done")

            self.url_ids = ids
            self.bow_sparse_matrix = bow
            self.feature_names = vectorizer.get_feature_names()  # mapping from url_id to url
            self.vocabulary = vectorizer.vocabulary_  # mapping from url to url_id
            self.shape = self.bow_sparse_matrix.shape

    def get_index(self, doc_id):
        return self.id2index[doc_id]

    def get_doc_id(self, index):
        return self.index2id[index]

    def get_feature_id(self, feature_name):
        return self.vocabulary.get(feature_name)

    def get_feature_name(self, feature_id):
        return self.feature_names[feature_id]

    def toarray(self):
        return self.bow_sparse_matrix.toarray()

    def to_uci(self, model_name='bow', save_folder=OUT_FOLDER):
        import os.path
        import codecs
        if self.bow_sparse_matrix is None:
            self.logger.error("Model is None.")
            return
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        filenames = model_name
        docword_name = os.path.join(save_folder,
                                    'docword.' + filenames + '.txt')
        vocab_name = os.path.join(save_folder, 'vocab.' + filenames + '.txt')
        with codecs.open(docword_name, 'w', encoding='utf-8') as docword_f, \
                codecs.open(vocab_name, 'w', encoding='utf-8') as vocab_f:
            urls_count = self.shape[0]
            words_count = self.shape[1]
            # Fill vocab_f file
            self.logger.info("Start filling {0}".format(vocab_name))
            for i in range(words_count):
                vocab_f.write(self.get_feature_name(i) + '\n')
            self.logger.info("Done.")
            # Fill docword_f file
            self.logger.info("Start filling {0}".format(docword_name))
            docword_f.write(str(urls_count) + '\n')
            docword_f.write(str(words_count) + '\n')
            docword_f.write(str(self.bow_sparse_matrix.nnz) + '\n')
            # nnz_position = docword_f.tell() # We fill this line later with nnz_counter.
            # nnz_counter = 0 # The number of nonzero counts in the bag-of-words.
            nnz_x, nnz_y = self.bow_sparse_matrix.nonzero()
            for x, y in zip(nnz_x, nnz_y):
                # nnz_counter += len(url_sparse_vector)
                docword_f.write(str(x + 1) + ' ' + str(y + 1) + ' ' + str(
                    self.bow_sparse_matrix[x, y]) + '\n')
            self.logger.info("Done.")
