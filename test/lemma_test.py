import spacy

text = "franchisee, franchisor, franchise, franchising"
nlp = spacy.load('en_core_web_lg')
doc = nlp(text)
for token in doc:
    print(token.lemma_)