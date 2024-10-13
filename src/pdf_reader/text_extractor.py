import pymupdf as fitz
from src.config import ReaderConfig
from src.pdf_reader.page import PaperPage
from typing import Generator, Tuple
import logging

logger = logging.getLogger("WFM.PdfReader")


class PdfReader:
    """
    Manages PDF operations and provides a generator to iterate through pages.
    """

    def __init__(self, config: ReaderConfig):
        self._config = config
        self._doc = None
        logger.info("PdfReader initialized")

    def set_path(self, path: str):
        """
        Update the configuration path.
        """
        self._config.set_config(path)
        logger.debug("PdfReader config updated")

    def open(self):
        """
        Open the PDF specified in the configuration path.
        """
        if not self._config.get("path"):
            raise ValueError("PDF path is not set in the configuration.")
        path = self._config.get("path")
        try:
            self._doc = fitz.open(path)
            logger.debug(f"PDF opened: {path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at path '{path}' was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while opening the PDF: {e}")

    def close(self):
        """
        Close the open PDF document, if any.
        """
        if self._doc:
            self._doc.close()
            self._doc = None
            logger.debug("PDF closed")
        else:
            raise ValueError("No PDF file is currently open.")

    def read(self) -> Generator[Tuple[int, PaperPage], None, None]:
        """
        Generator to yield each page of the open PDF as a PaperPage object.
        """
        self._ensure_document_open()

        for page_num in range(self._doc.page_count):
            try:
                fitz_page = self._doc.load_page(page_num)
                yield page_num + 1, PaperPage(fitz_page)
            except Exception as e:
                logger.warning(f"Error reading page {page_num + 1}: {e}")

    def _ensure_document_open(self):
        """
        Ensure the document is open, otherwise raise an error.
        """
        if not self._doc:
            raise ValueError("PDF file is not opened. Call 'open' first.")

    def __len__(self):
        return len(self._doc) if self._doc else 0

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
