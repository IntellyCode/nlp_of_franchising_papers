import pymupdf as fitz
from typing import List, Any, Generator
from logging import getLogger
logger = getLogger("WFM.Page")


class PaperPage:
    """
    A custom Page class that wraps around the fitz.Page object.
    Provides additional methods or properties as needed.
    """

    def __init__(self, fitz_page: fitz.Page):
        logger.debug("Initializing PaperPage")
        self._fitz_page = fitz_page

    def get_text(self, **kwargs):
        """
        Extract text from the page.
        You can pass fitz.Page.get_text() parameters via kwargs.
        """
        logger.debug(f"Extracting text from page")
        return self._fitz_page.get_text(**kwargs)
