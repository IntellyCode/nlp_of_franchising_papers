import spacy
from spacy.language import Language
from typing import List

from spacy.tokens.token import Token

from src.config import ProcessorConfig
from logging import getLogger
logger = getLogger("WFM.TextProcessor")


class Processor:

    def __init__(self, config: ProcessorConfig, model_name: str = 'en_core_web_sm') -> None:
        """
        Initializes the Processor with a specified spaCy language model.

        :param model_name: The name of the spaCy language model to load.
                           Default is 'en_core_web_sm'.
        """
        logger.info("Initializing Processor with spaCy language model.")
        try:
            self.nlp: Language = spacy.load(model_name)
            self._raw_text = None
            self._doc = None
            self._config: ProcessorConfig = config

            logger.debug(f"Loaded spaCy model: {model_name}")
        except Exception as e:
            logger.critical(f"Error loading spaCy model '{model_name}': {e}")

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
        logger.debug("Setting raw text")

    def process(self, stop_words=None) -> List[str]:
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

        _text = ""
        for token in self._doc:
            if not token.is_punct and not token.is_stop and not token.is_digit and token.is_alpha and self._custom_stopwards(token, stop_words):
                _text += f(token.lemma_) + ' '

        doc = self.nlp(_text)
        for chunk in doc.noun_chunks:
            words = chunk.text.split(" ")
            if not len(words) > 3:
                if len(words) > 1 and len(chunk.text) > 5:
                    _tokens.append(f(chunk.text))
                elif len(words) <= 1:
                    _tokens.append(f(chunk.text))

        logger.debug(f"Processed tokens: {_tokens}")
        return _tokens

    def _custom_stopwards(self, text: Token, stop_wards):
        if stop_wards is not None:
            for token in stop_wards:
                if token in text.text:
                    return False
        return True

if __name__ == '__main__':
    conf = ProcessorConfig()
    conf.set_config(capitalise=False)
    processor = Processor(conf, 'en_core_web_sm')
    text = "In 2023, Natural Language Processing (NLP) continues to evolve rapidly! Researchers focus on improving models like GPT-4, BERT, and others to achieve state-of-the-art performance in text understanding, generation, & translation. Some challenges in NLP include handling rare words, ambiguous meanings, and training models efficiently (with fewer resources). Popular frameworks, such as TensorFlow, PyTorch, & Hugging Face's Transformers, are used for training massive language models. Can we predict that by 2030, NLP systems will fully understand human emotions? Only time will tell... #AI #NLP #Future, Russia, Russian"
    processor.set_text(text)
    processed_tokens = processor.process()
    print(processed_tokens)
