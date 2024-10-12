from typing import Union, List, Dict, Optional
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from src.config import LdaConfig
from logging import getLogger
import pyLDAvis.gensim_models
logger = getLogger("WFM.Lda")


class Lda:
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
        logger.info("Initializing LDA class")

    def append_to_dtm(self, tokens: List):
        logger.debug(f"Appending tokens to DTM: {tokens}")
        ts = [token for token in tokens if len(token) > 1]
        self._dtm.append(ts)

    def _make_dictionary(self):
        """
        Makes a dictionary from the DTM.

        :return dictionary:
        """

        self._dictionary = corpora.Dictionary(self._dtm)
        logger.debug(f"No Below: {self._config.get('no_below')}; No Above: {self._config.get('no_above')}")
        self._dictionary.filter_extremes(no_below=self._config.get("no_below"), no_above=self._config.get("no_above"))
        self._corpus = [self._dictionary.doc2bow(doc) for doc in self._dtm]
        logger.debug('Number of unique tokens: %d' % len(self._dictionary))
        logger.debug('Number of documents: %d' % len(self._corpus))

    def train_model(self):
        """
        Train the LDA model on the corpus.
        :return:
        """
        self._make_dictionary()
        temp = self._dictionary[0] # only for dictionary loading
        id2word = self._dictionary.id2token

        self._model = LdaModel(
            corpus=self._corpus,
            id2word=id2word,
            chunksize=self._config.get("chunksize"),
            alpha=self._config.get("alpha"),
            eta=self._config.get("eta"),
            iterations=self._config.get("iterations"),
            num_topics=self._config.get("num_topics"),
            passes=self._config.get("passes"),
            eval_every=self._config.get("eval_every"),
        )
        logger.debug("LDA model trained")

    def get_topics(self):
        """
        Get topics from trained model.

        :return top_topics: List of topics and their frequencies (probabilities)
        """
        if self._models is None:
            raise AttributeError('No models has been trained.')

        top_topics = self._model.top_topics(self._corpus)
        logger.debug(f"Top Topics: {top_topics} ")
        return top_topics

    def visualise(self, file_path: str):
        """
        Visualise the LDA model.
        :param file_path: a path to an HTML file
        :return:
        """
        vis = pyLDAvis.gensim_models.prepare(self._model, self._corpus,
                                             self._dictionary, mds="mmds")
        pyLDAvis.save_html(vis, file_path)
        logger.info(f"Visualizing LDA model at path: {file_path}")
