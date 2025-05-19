import re
from string import punctuation

PATTERN = re.compile(r"^(?=.*[^A-Za-z]).+$")  # General malformated words
MIXED_ALPHA_NUM_START = re.compile(r'^\d+[a-zA-Z]+$')
MIXED_ALPHA_NUM_END = re.compile(r'^[a-zA-Z]+\d+$')
SPLIT_ALPHA_NUM = re.compile(r'\d+|[a-zA-Z]+')
GARBAGE_PATTERNS = [
    re.compile(r'^_+$'),           # Only underscores
    re.compile(r'^-+$'),           # Only dashes
    re.compile(r'^=+$'),           # Only equals
    re.compile(r'^\*+$'),          # Only asterisks
    re.compile(r'^\(cid:\d+\)$'),  # PDF (cid:23) artifacts
    re.compile(r'^page\s*\d+$', re.IGNORECASE),    # Page numbers
    re.compile(r'^figure\s*\d+$', re.IGNORECASE),  # Figures
    re.compile(r'^table\s*\d+$', re.IGNORECASE),   # Tables
]
REPEATED_GARBAGE_PATTERN = re.compile(r'^[_\-=*]+$')
REPEATED_GARBAGE_PATTERN_v2 = re.compile(r'^[_\-=*.]{2,}$')


def filter_doc(doc):
    return [
        token.lemma_.lower() for token in doc
        if (not token.is_stop and
            not token.is_punct and
            not token.like_email and
            not token.like_url and
            not token.like_num and
            not token.is_space and
            token.ent_type_ != "PERSON" and
            token.pos_ != "PROPN" and
            len(token.text) > 2 and
            not re.match(PATTERN, token.text))
    ]


def filter_doc_light(doc):
    clean_tokens = []
    for token in doc:
        if token.like_email or token.like_url or token.is_space:
            continue
        text = token.text.lower()
        if text.startswith('tel:') or text.startswith('fax:'):
            continue
        if REPEATED_GARBAGE_PATTERN.match(text) or REPEATED_GARBAGE_PATTERN_v2.match(text):
            continue
        if MIXED_ALPHA_NUM_START.match(text) or MIXED_ALPHA_NUM_END.match(text):
            split_text = SPLIT_ALPHA_NUM.findall(text)
            clean_tokens.extend(split_text)
        else:
            clean_tokens.append(text)
    return clean_tokens


def smart_join(tokens, punct=punctuation):
    text = ''
    for i, token in enumerate(tokens):
        if i > 0 and token not in punct:
            text += ' '
        text += token
    return text


def lemmatizer(nlp, doc):
    return [
        token.lemma_.lower() for token in nlp(doc)
        if not token.is_punct and not token.is_stop
    ]