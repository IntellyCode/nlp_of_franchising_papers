import spacy
from spacy.language import Language
from typing import List
from src.config import ProcessorConfig


class Processor:

    def __init__(self, config: ProcessorConfig, model_name: str = 'en_core_web_sm') -> None:
        """
        Initializes the Processor with a specified spaCy language model.

        :param model_name: The name of the spaCy language model to load.
                           Default is 'en_core_web_sm'.
        """
        try:
            self.nlp: Language = spacy.load(model_name)
            self._raw_text = None
            self._doc = None
            self._config: ProcessorConfig = config
            print(f"Loaded spaCy model: {model_name}")
        except Exception as e:
            print(f"Error loading spaCy model '{model_name}': {e}")

    def get_doc(self):
        """
        :return doc: Spacy Document object
        """
        if self._doc is None:
            raise Exception("Spacy Document is not loaded")
        return self._doc

    def get_text(self):
        """
        :return raw_text: Spacy Document object
        """
        if self._raw_text is None:
            raise Exception("Spacy Document is not loaded")
        return self._raw_text

    def set_text(self, raw_text):
        self._raw_text = raw_text
        self._doc = self.nlp(raw_text)

    def process(self) -> List[str]:
        """
        Process the Spacy Doc object by performing the following:
            1. Remove punctuations, numbers, and special characters.
            2. Remove stop words.
            3. Lemmatize the remaining tokens.

        :return processed_tokens: List of tokens from the doc.
        """
        _tokens = []
        if not self._config.get("capitalise"):
            f = str.lower
        else:
            f = lambda x: x

        for token in self._doc:
            if not token.is_punct and not token.is_stop and not token.is_digit and token.is_alpha:
                _tokens.append(f(token.lemma_))

        return _tokens


if __name__ == '__main__':
    conf = ProcessorConfig()
    conf.set_config({"capitalise": False})
    processor = Processor(conf, 'en_core_web_sm')
    text = "In 2023, Natural Language Processing (NLP) continues to evolve rapidly! Researchers focus on improving models like GPT-4, BERT, and others to achieve state-of-the-art performance in text understanding, generation, & translation. Some challenges in NLP include handling rare words, ambiguous meanings, and training models efficiently (with fewer resources). Popular frameworks, such as TensorFlow, PyTorch, & Hugging Face's Transformers, are used for training massive language models. Can we predict that by 2030, NLP systems will fully understand human emotions? Only time will tell... #AI #NLP #Future"
    processor.set_text(text)
    processed_tokens = processor.process()
    print(processed_tokens)
