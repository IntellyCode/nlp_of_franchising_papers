from abc import abstractmethod, ABC

import numpy as np
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer, models
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
import torch
import gc

from .loss_functions import topic_outlier_loss, coherence_loss, outlier_coherence_density_loss, coherence_n_topics_loss


class Objective(ABC):
    def __init__(self, docs, seed, analyzer="word", gpu=True):
        """
        Base objective class.
        """
        if torch.cuda.is_available() and gpu:
            torch.cuda.empty_cache()
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.docs = docs
        self.seed = seed
        self.analyzer = analyzer
        self.vectorizer = None

    @abstractmethod
    def __call__(self, hyperparams):
        """
        This method must be overridden by subclasses.
        It should take hyperparameters as input and return a dict with at least 'loss' and 'status'.
        """
        pass

    def _clean_up(self):
        """
        Performs cleanup by collecting garbage and emptying the CUDA cache.
        """
        gc.collect()
        try:
            torch.cuda.empty_cache()
        except ImportError:
            pass

    def train(self, hyperparams, calc_prob=False):
        # Fit the vectorizer for better topic representation
        self.vectorizer = CountVectorizer(
            stop_words='english',
            analyzer=self.analyzer,
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 3),
        )
        self.vectorizer.fit(self.docs)

        # Create the embedding model
        embedding_model_name = hyperparams["embedding_model"]
        transformer_model = models.Transformer(embedding_model_name)
        pooling_model = models.Pooling(
            transformer_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True
        )
        embedding_model = SentenceTransformer(
            modules=[transformer_model, pooling_model],
            device=self.device
        )

        # Create UMAP model
        umap_params = hyperparams["umap_model"]
        umap_params['n_neighbors'] = int(umap_params['n_neighbors'])
        umap_params['n_components'] = int(umap_params['n_components'])
        umap_model = UMAP(
            **umap_params,
            n_jobs=-1,
            random_state=self.seed
        )

        # Create HDBSCAN model
        hdbscan_params = hyperparams["hdbscan_model"]
        hdbscan_params['min_cluster_size'] = int(hdbscan_params['min_cluster_size'])
        hdbscan_params['min_samples'] = int(hdbscan_params['min_samples'])
        hdbscan_model = HDBSCAN(
            **hdbscan_params,
            core_dist_n_jobs=-1,
            prediction_data=calc_prob
        )

        # Train BERTopic
        topic_model = BERTopic(
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            embedding_model=embedding_model,
            vectorizer_model=self.vectorizer,
            verbose=False,
            calculate_probabilities=calc_prob
        )
        topics, probabilities = topic_model.fit_transform(self.docs)
        return topics, probabilities, topic_model, hdbscan_model, umap_model, embedding_model


class MTObjective(Objective):
    def __call__(self, hyperparams):
        np.random.seed(self.seed)
        try:
            topics, probabilities, topic_model, hdbscan_model, umap_model, embedding_model = self.train(hyperparams)

            # Calculate number of outliers and topics
            num_outliers = topics.count(-1)
            unique_topics = set(topics)
            if -1 in unique_topics:
                unique_topics.remove(-1)
            num_topics = len(unique_topics)
            total_docs = len(self.docs)

            loss = topic_outlier_loss(num_outliers, num_topics, total_docs)

            # Clean Up
            del topic_model, hdbscan_model, umap_model, embedding_model
            self.vectorizer = None
            self._clean_up()

            return {
                'loss': loss,
                'status': 'ok',
                'hyperparams': hyperparams,
                'num_topics': num_topics,
                'num_outliers': num_outliers,
            }
        except Exception as e:
            print(f"Error with params {hyperparams}: {e}")
            return {
                'loss': 1e10,
                'status': 'ok',
                'hyperparams': hyperparams,
                'error': str(e),
            }


class CLObjective(Objective):
    def __init__(self, docs, seed, analyzer="word", gpu=True, top_n=20):
        super(CLObjective, self).__init__(docs, seed, analyzer, gpu)
        self.top_n = top_n

    def __call__(self, hyperparams):
        np.random.seed(self.seed)
        try:
            topics, probabilities, topic_model, hdbscan_model, umap_model, embedding_model = self.train(hyperparams)

            topic_dict = topic_model.get_topics()
            topics = []
            for topic_id, word_scores in topic_dict.items():
                if topic_id == -1:
                    continue
                top_words = [word for word, score in word_scores][:self.top_n]
                topics.append(top_words)

            tokenized_docs = [doc.split() for doc in self.docs]
            print("Topics structure:", topics)
            loss = coherence_loss(tokenized_docs, {"topics": topics})

            # Clean Up
            del topic_model, hdbscan_model, umap_model, embedding_model, tokenized_docs
            self.vectorizer = None
            self._clean_up()

            return {
                'loss': loss,
                'status': 'ok',
                'hyperparams': hyperparams
            }
        except Exception as e:
            print(f"Error with params {hyperparams}: {e}")
            return {
                'loss': 1e10,
                'status': 'ok',
                'hyperparams': hyperparams,
                'error': str(e),
            }


class OCDObjective(CLObjective):
    def __call__(self, hyperparams):
        np.random.seed(self.seed)
        try:
            topics_bert, probabilities, topic_model, hdbscan_model, umap_model, embedding_model = self.train(hyperparams, calc_prob=True)

            topic_dict = topic_model.get_topics()
            topics = []
            for topic_id, word_scores in topic_dict.items():
                if topic_id == -1:
                    continue
                top_words = [word for word, score in word_scores][:self.top_n]
                topics.append(top_words)

            tokenized_docs = [doc.split() for doc in self.docs]
            loss = outlier_coherence_density_loss(tokenized_docs, {"topics": topics}, topics_bert, probabilities)

            # Clean Up
            del topic_model, hdbscan_model, umap_model, embedding_model, tokenized_docs
            self.vectorizer = None
            self._clean_up()

            return {
                'loss': loss,
                'status': 'ok',
                'hyperparams': hyperparams
            }
        except Exception as e:
            print(f"Error with params {hyperparams}: {e}")
            return {
                'loss': 1e10,
                'status': 'ok',
                'hyperparams': hyperparams,
                'error': str(e),
            }


class CNTObjective(CLObjective):
    def __call__(self, hyperparams):
        np.random.seed(self.seed)
        try:
            topics_bert, probabilities, topic_model, hdbscan_model, umap_model, embedding_model = self.train(hyperparams, calc_prob=True)

            topic_dict = topic_model.get_topics()
            topics = []
            for topic_id, word_scores in topic_dict.items():
                if topic_id == -1:
                    continue
                top_words = [word for word, score in word_scores][:self.top_n]
                topics.append(top_words)

            tokenized_docs = [doc.split() for doc in self.docs]
            loss = coherence_n_topics_loss(tokenized_docs, {"topics": topics}, topics_bert)

            # Clean Up
            del topic_model, hdbscan_model, umap_model, embedding_model, tokenized_docs
            self.vectorizer = None
            self._clean_up()

            return {
                'loss': loss,
                'status': 'ok',
                'hyperparams': hyperparams
            }
        except Exception as e:
            print(f"Error with params {hyperparams}: {e}")
            return {
                'loss': 1e10,
                'status': 'ok',
                'hyperparams': hyperparams,
                'error': str(e),
            }