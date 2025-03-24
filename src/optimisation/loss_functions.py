from octis.evaluation_metrics.coherence_metrics import Coherence
import numpy as np


def topic_outlier_loss(num_outliers, num_topics, total_docs, t_target=None, w1=1.0, w2=1.0, desired_docs_per_topic=15):
    """
    Custom loss function that minimises number of topics and number of outliers

    :param num_outliers: Number of documents classified as outliers.
    :param num_topics: Number of topics discovered by the model.
    :param total_docs: Total number of documents in the dataset.
    :param t_target: Target topics-to-docs ratio. If None, computed from desired_docs_per_topic.
    :param w1: Weight for the outlier penalty. Default is 1.0.
    :param w2: Weight for the topic count penalty. Default is 1.0.
    :param desired_docs_per_topic: Desired number of documents per topic if t_target is None.
    :return: Computed loss value.
    """
    if total_docs == 0:
        raise ValueError("Total number of documents must be greater than zero.")

    if t_target is None:
        t_target = 1.0 / desired_docs_per_topic

    outlier_ratio = num_outliers / total_docs
    topic_ratio = num_topics / total_docs

    outlier_penalty = w1 * outlier_ratio
    topic_penalty = w2 * abs(topic_ratio - t_target)

    loss = outlier_penalty + topic_penalty
    return loss


def coherence_loss(corpus, output):
    coherence_metric = Coherence(texts=corpus, measure="c_v")
    score = coherence_metric.score(output)
    return -score


def outlier_coherence_density_loss(corpus, output, topics, doc_probs, target_density=3, prob_threshold=0.1):
    """
    Computes the loss of a topic model based on coherence, number of outliers and topic density
    :param corpus: The tokenized corpus
    :param output: Topic model output for coherence metric
    :param topics: Topics from Bert
    :param doc_probs: Probabilities form Bert
    :param target_density: How many topics per paper on average?
    :param prob_threshold: Does the document contain said topic (if probability > threshold then yes)
    :return: (float) loss
    """

    coherence_metric = Coherence(texts=corpus, measure="c_v")
    coherence = coherence_metric.score(output)
    total_docs = len(topics)
    outlier_docs = sum(1 for t in topics if t == -1)
    outlier_ratio = outlier_docs / total_docs
    active_topic_counts = [sum(1 for prob in probs if prob > prob_threshold) for probs in doc_probs]
    avg_active_topics = sum(active_topic_counts) / len(active_topic_counts)
    density_penalty = min(abs(avg_active_topics - target_density) / target_density, 1.0)
    loss = (1 - coherence) + outlier_ratio + density_penalty
    return loss


def coherence_n_topics_loss(corpus, output, topics):
    coherence_metric = Coherence(texts=corpus, measure="c_v")
    coherence = coherence_metric.score(output)

    unique_topics = set(t for t in topics if t != -1)
    topic_count = len(unique_topics)
    topic_density = topic_count / len(topics)

    loss = -(coherence + topic_density)
    return loss
