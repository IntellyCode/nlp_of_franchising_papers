import gc

import numpy as np
import torch
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer, models
from umap import UMAP


class BertModel:
    def __init__(self, docs, seed, analyzer="word", gpu=True):
        if torch.cuda.is_available() and gpu:
            torch.cuda.empty_cache()
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.docs = docs
        self.seed = seed
        self.analyzer = analyzer
        self.gpu = gpu
        self.vectorizer = None
        self.topic_model = None

    def assemble(self, hyperparams):
        np.random.seed(self.seed)
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
        self.topic_model = BERTopic(
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            embedding_model=embedding_model,
            vectorizer_model=self.vectorizer,
            verbose=True)

        # Clean Up
        del hdbscan_model, umap_model, embedding_model
        self.vectorizer = None
        self._clean_up()

        return self.topic_model.fit_transform(self.docs)

    def _clean_up(self):
        gc.collect()
        try:
            torch.cuda.empty_cache()
        except ImportError:
            pass



