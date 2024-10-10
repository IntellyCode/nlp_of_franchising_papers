import pandas as pd
from typing import List
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np


class BagOfWords:
    def __init__(self):
        """
        Initialize the BagOfWords class with an empty pandas DataFrame.

        The DataFrame (self._df) will have:
            - Rows representing documents, indexed by `row_name`.
            - Columns representing unique words (tokens) across all documents.
            - Cell values representing the frequency of the word in the document.
        """
        self._df = pd.DataFrame()

    def add_entry(self, row_name: str,  tokens: List[str],):
        """
        Add a new document entry to the Document-Term Matrix (DTM).

        Parameters:
        - tokens (List[str]): A list of processed tokens (words) from the document.
        - row_name (str): The unique identifier for the document (used as the row index).
        """
        token_counts = Counter(tokens)
        new_words = set(token_counts.keys()) - set(self._df.columns)

        if new_words:
            for word in new_words:
                self._df[word] = 0

        new_row = {word: 0 for word in self._df.columns}

        for word, count in token_counts.items():
            new_row[word] = count
        new_row_df = pd.DataFrame([new_row], index=[row_name])
        self._df = pd.concat([self._df, new_row_df], axis=0)

    def compress(self, threshold: float = 0.1):
        """
        Compress the Document-Term Matrix (DTM) by applying TF-IDF and removing words
        with TF-IDF scores below the specified threshold. Instead of deleting columns,
        it sets the cell values to 0. After compression, it removes any columns that
        contain only 0s.

        Parameters:
        - threshold (float): The TF-IDF score below which a word's frequency is set to 0.
                               Must be between 0 and 1. Default is 0.1.
        """
        if self._df.empty:
            print("The Document-Term Matrix is empty. No compression needed.")
            return

        transformer = TfidfTransformer()
        tfidf_matrix = transformer.fit_transform(self._df)
        tfidf_dense = tfidf_matrix.toarray()
        mask = tfidf_dense < threshold

        self._df = self._df.mask(mask, 0)
        self._df = self._df.astype(int)

        zero_columns = self._df.columns[(self._df == 0).all()]
        if not zero_columns.empty:
            self._df = self._df.drop(columns=zero_columns)

    def get_df(self) -> pd.DataFrame:
        """
        Retrieve the current Document-Term Matrix (DTM) as a pandas DataFrame.

        Returns:
        - pd.DataFrame: The DTM with documents as rows and words as columns.
        """
        return self._df

    def __str__(self):
        """
        Return a string representation of the Document-Term Matrix.
        """
        return str(self._df)

    def __repr__(self):
        """
        Return an official string representation of the Document-Term Matrix.
        """
        return self._df.__repr__()


if __name__ == '__main__':
    bow = BagOfWords()
    processed_tokens = ['Natural', 'Natural', 'Natural', 'Language', 'Language', 'Language','Processing', 'NLP', 'continue', 'evolve', 'rapidly', 'researcher', 'focus', 'improve', 'model', 'like', 'BERT', 'achieve', 'state', 'art', 'performance', 'text', 'understanding', 'generation', 'translation', 'challenge', 'NLP', 'include', 'handle', 'rare', 'word', 'ambiguous', 'meaning', 'training', 'model', 'efficiently', 'few', 'resource', 'popular', 'framework', 'TensorFlow', 'PyTorch', 'Hugging', 'Face', 'Transformers', 'train', 'massive', 'language', 'model', 'predict', 'NLP', 'system', 'fully', 'understand', 'human', 'emotion', 'time', 'tell', 'ai', 'nlp', 'future']
    # Add the processed tokens to BagOfWords with a row name
    bow.add_entry("Document_1", processed_tokens)
    # bow.add_entry("Document_2", processed_tokens+["testing","testing","testing","testing"])

    # Print the Document-Term Matrix
    print("Document-Term Matrix after adding Document_1:")
    print(bow)

    bow.compress(threshold=0.2)
    print("DTM after compression:")
    print(bow)