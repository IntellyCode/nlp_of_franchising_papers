def topic_transform(topic_dict, top_n):
    topics = []
    for topic_id, word_scores in topic_dict.items():
        if topic_id == -1:
            continue
        top_words = [word for word, score in word_scores][:top_n]
        topics.append(top_words)
    return topics
