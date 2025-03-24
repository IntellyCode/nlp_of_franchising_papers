from hyperopt import hp


def basic_space():
    return {
        'embedding_model': hp.choice('embedding_model', [
            'allenai/scibert_scivocab_uncased',
            'sentence-transformers/all-MiniLM-L6-v2',
            'sentence-transformers/paraphrase-MiniLM-L3-v2'
        ]),
        'umap_model': {
            'n_neighbors': hp.quniform('n_neighbors', 1, 50, 1),
            'n_components': hp.quniform('n_components', 1, 15, 1),
            'min_dist': hp.uniform('min_dist', 0.0, 1.0),
            'metric': hp.choice('metric', ['cosine', 'euclidean', 'manhattan']),
        },
        'hdbscan_model': {
            'min_cluster_size': hp.quniform('min_cluster_size', 1, 50, 1),
            'min_samples': hp.quniform('min_samples', 1, 20, 1),
        }
    }
