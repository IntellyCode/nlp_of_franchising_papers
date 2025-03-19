import re


pattern = re.compile(r"^(?=.*[^A-Za-z]).+$")


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
            not re.match(pattern, token.text))
    ]