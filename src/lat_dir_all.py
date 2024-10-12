import pandas as pd
from typing import Union, List, Dict, Optional
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import warnings
from src.config import LdaConfig
from pprint import pprint


class LatDirAll:
    def __init__(self, config: LdaConfig):
        """
        Initialize the LatDirAll class with no DTM and no trained models.
        """
        self._dtm = []
        self._config = config
        self._model = None
        self._dictionary: Optional[corpora.Dictionary] = None
        self._corpus: List[List[tuple]] = []
        self._models: Union[LdaModel, Dict[int, LdaModel]] = {}

    def append_to_dtm(self, tokens: List):
        ts = [token for token in tokens if len(token) > 1]
        self._dtm.append(ts)

    def _make_dictionary(self):
        """
        Makes a dictionary from the DTM.

        :return dictionary:
        """

        self._dictionary = corpora.Dictionary(self._dtm)
        self._dictionary.filter_extremes(no_below=self._config.get("extremes")[0], no_above=self._config.get("extremes")[1])
        self._corpus = [self._dictionary.doc2bow(doc) for doc in self._dtm]
        print('Number of unique tokens: %d' % len(self._dictionary))
        print('Number of documents: %d' % len(self._corpus))

    def train_model(self):
        self._make_dictionary()
        # Set training parameters.
        num_topics = 20
        chunksize = 30
        passes = 20
        iterations = 400
        eval_every = None  # Don't evaluate model perplexity, takes too much time.

        # Make an index to word dictionary.
        temp = self._dictionary[0]
        id2word = self._dictionary.id2token
        # print("Dictionary: ", self._dictionary)
        # print("Corpus: ", self._corpus)
        # print("Id 2 words: ", id2word)

        self._model = LdaModel(
            corpus=self._corpus,
            id2word=id2word,
            chunksize=chunksize,
            alpha='auto',
            eta='auto',
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=eval_every
        )

    def get_topics(self):
        if self._models is None:
            raise AttributeError('No models has been trained.')

        top_topics = self._model.top_topics(self._corpus)
        pprint(top_topics)
        return top_topics

    def get_corpus(self):
        return self._corpus

    def get_dictionary(self):
        return self._dictionary

    def get_model(self):
        return self._model
if __name__ == '__main__':
    from src.bag_of_words import BagOfWords
    bow = BagOfWords()
    processed_tokens = ['Natural', 'Natural', 'Natural', 'Language', 'Language', 'Language','Processing', 'NLP', 'continue', 'evolve', 'rapidly', 'researcher', 'focus', 'improve', 'model', 'like', 'BERT', 'achieve', 'state', 'art', 'performance', 'text', 'understanding', 'generation', 'translation', 'challenge', 'NLP', 'include', 'handle', 'rare', 'word', 'ambiguous', 'meaning', 'training', 'model', 'efficiently', 'few', 'resource', 'popular', 'framework', 'TensorFlow', 'PyTorch', 'Hugging', 'Face', 'Transformers', 'train', 'massive', 'language', 'model', 'predict', 'NLP', 'system', 'fully', 'understand', 'human', 'emotion', 'time', 'tell', 'ai', 'nlp', 'future']
    # Add the processed tokens to BagOfWords with a row name
    conf = LdaConfig()
    conf.set_config({"alpha":0.1, "beta":0.3})
    lat_dir_all = LatDirAll(conf)
    lat_dir_all.append_to_dtm(processed_tokens)
    lat_dir_all.train_model()
    lat_dir_all.get_topics()
