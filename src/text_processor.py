import spacy
from spacy.language import Language
from spacy.tokens import Doc
from typing import List, Optional
from bag_of_words import BagOfWords


class Processor:
    def __init__(self, model_name: str = 'en_core_web_sm') -> None:
        """
        Initializes the Processor with a specified spaCy language model.

        :param model_name: The name of the spaCy language model to load.
                           Default is 'en_core_web_sm'.
        """
        try:
            self.nlp: Language = spacy.load(model_name)
            print(f"Loaded spaCy model: {model_name}")
        except Exception as e:
            print(f"Error loading spaCy model '{model_name}': {e}")

    def _process_text(self, text: str) -> Optional[Doc]:
        """
        Processes the input text using the spaCy language model.

        :param text: The input text to be processed.
        :return: A spaCy Doc object containing the processed text, or None if text is empty.
        """
        if not text:
            print("No text provided for processing.")
            return None

        # Process the text using the spaCy language model
        doc = self.nlp(text)
        return doc

    def filter_tokens_by_pos(self, text: str, pos_tag: str) -> List[str]:
        """
        Filters tokens from the processed text based on the specified POS tag.

        :param text: The input text to be processed and filtered.
        :param pos_tag: The part-of-speech tag to filter tokens by (e.g., 'NOUN', 'VERB').
        :return: A list of token texts with the specified POS tag.
        """
        doc = self._process_text(text)
        if doc:
            filtered_tokens: List[str] = [token.text for token in doc if token.pos_ == pos_tag]
            return filtered_tokens
        return []

    def exclude_tokens_by_pos(self, text: str, pos_tags: List[str]) -> Optional[Doc]:
        """
        Excludes tokens with the specified POS tags from the processed text.

        :param text: The input text to be processed.
        :param pos_tags: A list of POS tags to exclude (e.g., ['NOUN', 'VERB']).
        :return: A spaCy Doc object with tokens that do not have the specified POS tags.
        """
        doc = self._process_text(text)
        if not doc:
            return None

        # Rebuild text excluding tokens with specified POS tags
        filtered_text = " ".join(token.text for token in doc if token.pos_ not in pos_tags)

        # Process the filtered text into a new Doc object
        return self.nlp(filtered_text)


# Example usage
if __name__ == "__main__":
    processor = Processor()  # Initializes with the English model by default
    text = """
        Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and humans through natural language. The ultimate goal of NLP is to enable computers to understand, interpret, and respond to human language in a way that is both meaningful and useful. This field combines computational linguistics, which models the structure of human language, with machine learning, deep learning, and statistical methods.
    
        NLP encompasses several important tasks such as text classification, sentiment analysis, machine translation, named entity recognition, and speech recognition, among others. For example, text classification is the process of assigning categories or labels to text based on its content. This is widely used in email filtering, where emails are automatically categorized as spam or not spam. Sentiment analysis, on the other hand, is used to determine the sentiment or emotion expressed in a piece of text, which is particularly useful in monitoring social media and customer feedback.
        
        One of the key challenges in NLP is dealing with the ambiguity and variability of human language. Words can have multiple meanings depending on the context, and different people can express the same idea in numerous ways. This makes tasks like machine translation particularly difficult because the system must not only understand the literal meaning of the words but also capture the nuances of the original message.
        
        Modern NLP techniques rely heavily on deep learning methods, particularly neural networks, which have been shown to perform exceptionally well on a variety of language tasks. Models such as Transformers, including the famous BERT and GPT, have set new benchmarks in many NLP applications. These models use attention mechanisms that allow them to weigh the importance of different parts of the input text, leading to better understanding and generation of language.
        
        Another significant aspect of NLP is named entity recognition (NER), which involves identifying and classifying key elements in text into predefined categories such as names of people, organizations, locations, expressions of time, quantities, monetary values, percentages, and more. NER is crucial for information extraction tasks where specific data needs to be pulled out from large volumes of text, such as in legal documents or research papers.
        
        Speech recognition, which converts spoken language into text, is another critical component of NLP. It powers various applications, including virtual assistants like Siri and Alexa, dictation software, and transcription services. Achieving high accuracy in speech recognition is challenging due to factors like accents, pronunciation variations, background noise, and homophones.
        
        Another emerging area in NLP is conversational AI, which focuses on building systems that can carry on a dialogue with humans. Chatbots and virtual assistants are prime examples of conversational AI. These systems need to understand user inputs, maintain context across multiple exchanges, and generate appropriate responses. They leverage various NLP tasks such as intent recognition, dialogue management, and natural language generation to simulate a human-like conversation.
        
        Tokenization, stemming, and lemmatization are fundamental preprocessing steps in NLP. Tokenization involves breaking down text into individual words or phrases, which are the building blocks for further analysis. Stemming reduces words to their root form, while lemmatization goes a step further by reducing words to their base or dictionary form. These steps help standardize the input text, making it easier for models to learn from it.
        
        Despite the advancements, NLP still faces many challenges. One major challenge is bias in training data, which can lead to biased models that produce unfair or prejudiced outcomes. Another challenge is the need for vast amounts of labeled data for training supervised models, which can be expensive and time-consuming to obtain. Additionally, language diversity poses a significant hurdle, as most NLP research and tools are centered around English, leaving many other languages underrepresented.
        
        As NLP continues to evolve, it is likely to become even more integrated into our daily lives. From improving customer service through chatbots to assisting in medical diagnoses by analyzing patient records, the potential applications of NLP are vast and varied. Researchers are continuously working on making NLP models more efficient, less resource-intensive, and better at understanding the complexities of human language.
        
        In conclusion, Natural Language Processing is a rapidly growing field that has made significant strides in recent years. With ongoing advancements in machine learning and deep learning, the capabilities of NLP systems are expanding, bringing us closer to the goal of seamless human-computer communication. However, there is still much work to be done to overcome the challenges and ensure that these technologies are accessible and fair for all.
    """
    tags = ["ADP","AUX","CCONJ","DET","INTJ","NUM","PART","PRON","PUNCT","SCONJ","SYM","X"]
    filtered_text = processor.exclude_tokens_by_pos(text, tags)
    bow = BagOfWords(filtered_text)
    dict = bow.extract_frequencies()
    sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    print(sorted_dict)
