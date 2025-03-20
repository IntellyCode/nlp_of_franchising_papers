import numpy as np
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer, models
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
import torch
import gc

from .loss_functions import topic_outlier_loss


class MTObjective:

    def __init__(self, actual_docs, preprocessed_docs, seed, analyzer="word", gpu=True):
        """
        MTObjective - Minimizes Number of Topics and Outliers during hyperparameter optimization.

        Designed to work with Hyperopt. The __call__ method receives hyperparameters,
        trains the BERTopic model and returns the loss based on
        the custom loss function.
        """
        if torch.cuda.is_available() and gpu:
            torch.cuda.empty_cache()
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.actual_docs = actual_docs
        self.preprocessed_docs = preprocessed_docs
        self.seed = seed
        self.analyzer = analyzer
        self.vectorizer = None

    def __call__(self, hyperparams):
        np.random.seed(self.seed)
        try:
            # Use Preprocessed Corpus?
            preprocess = hyperparams["preprocess"]
            docs = (self.preprocessed_docs if preprocess else self.actual_docs).copy()

            # Fit the vectorizer for better topic representation
            self.vectorizer = CountVectorizer(
                analyzer=self.analyzer,
                min_df=2,
                max_df=0.95,
                ngram_range=(1, 3),
            )
            self.vectorizer.fit(docs)

            # Create the embedding model
            embedding_model_name = hyperparams["embedding_model"]
            transformer_model = models.Transformer(embedding_model_name)
            pooling_model = models.Pooling(
                transformer_model.get_word_embedding_dimension(),
                pooling_mode_mean_tokens=True
            )
            embedding_model = SentenceTransformer(modules=[transformer_model, pooling_model], device=self.device)

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

            )

            # Train Bert
            topic_model = BERTopic(
                umap_model=umap_model,
                hdbscan_model=hdbscan_model,
                embedding_model=embedding_model,
                vectorizer_model=self.vectorizer,
                verbose=False)
            topics, probabilities = topic_model.fit_transform(docs)

            num_outliers = topics.count(-1)
            unique_topics = set(topics)
            if -1 in unique_topics:
                unique_topics.remove(-1)
            num_topics = len(unique_topics)
            total_docs = len(docs)

            loss = topic_outlier_loss(num_outliers, num_topics, total_docs)

            # Clean Up
            del docs, topic_model, hdbscan_model, umap_model, embedding_model
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

    def _clean_up(self):
        gc.collect()
        try:
            torch.cuda.empty_cache()
        except ImportError:
            pass
