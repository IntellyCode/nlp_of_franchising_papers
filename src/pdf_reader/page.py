import pymupdf as fitz
from logging import getLogger
from difflib import get_close_matches
from src.config import special_character
from collections import defaultdict
logger = getLogger("WFM.Page")


def contains_keywords(text, similarity_threshold=0.9, keywords=("references", "bibliography", "sources", "works cited")):
    words = text.split()

    for word in words:
        first_letter_matches = [kw for kw in keywords if kw[0].lower() == word[0].lower()]
        if get_close_matches(word.lower(), first_letter_matches, n=1, cutoff=similarity_threshold):
            return True
    return False


class PaperPage:
    """
    A custom Page class that wraps around the fitz.Page object.
    Provides additional methods or properties as needed.
    """

    def __init__(self, fitz_page: fitz.Page):
        logger.debug("Initializing PaperPage")
        self._fitz_page = fitz_page
        self.text = None

    def _spans(self):
        for block in self._fitz_page.get_text("dict")["blocks"]:
            if block['type'] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        yield span

    def _compare_none(self, v1, v2=None):
        if v2 is None:
            return True
        elif v1 == v2:
            return True
        return False

    def _in_middle(self, rect):
        page_width, page_height = self._fitz_page.rect.width, self._fitz_page.rect.height
        left_bound = page_width * 0.1
        right_bound = page_width * 0.9
        top_bound = page_height * 0.25
        bottom_bound = page_height * 0.75

        return (left_bound <= rect[0] <= right_bound and
                left_bound <= rect[2] <= right_bound and
                top_bound <= rect[1] <= bottom_bound and
                top_bound <= rect[3] <= bottom_bound)

    def get_font(self):
        result = defaultdict(int)
        for span in self._spans():
            if self._in_middle(span["bbox"]):
                result[str(span["size"])] += 1
                result[str(span["font"])] += 1
        return result

    def get_text(self, find_references=True, **kwargs):
        """
        Extract text from the page.
        :param:
        **kwargs (dict): font size and font type to select only text with this criteria

        :return: str: The text extracted from the page.
        """
        found_references = False
        fontsize = None
        fonttype = None
        for key in kwargs.keys():
            if "fontsize" == key:
                fontsize = kwargs[key]
            if "fonttype" == key:
                fonttype = kwargs[key]

        string = ""
        for span in self._spans():
            text = span["text"]
            font_size = span["size"]
            font_type = span["font"]
            if find_references and contains_keywords(text):
                if "bold" in font_type.lower() and self._compare_none(font_size, fontsize):
                    found_references = True
            if not found_references:
                if self._compare_none(font_size, fontsize) and self._compare_none(font_type, fonttype) and len(text) > 3:
                    string += text
        self.text = string
        if find_references:
            return found_references, string
        else:
            return string

    def __str__(self):
        return self.text
