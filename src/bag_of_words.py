from spacy.tokens import Doc
from typing import Dict


class BagOfWords:
    def __init__(self, doc: Doc):
        self._doc = doc
        self._word_frequencies = None

    def extract_frequencies(self):
        """
        Extracts word frequencies from the document.

        :return: A dictionary with words as keys and their frequency as values.
        """
        if self._word_frequencies is None:
            word_frequencies: Dict[str, int] = {}
            for token in self._doc:
                if not token.is_space:
                    word = token.text.lower()
                    if word in word_frequencies:
                        word_frequencies[word] += 1
                    else:
                        word_frequencies[word] = 1
            self._word_frequencies = word_frequencies
        return self._word_frequencies


