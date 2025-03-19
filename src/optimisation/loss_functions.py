

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
