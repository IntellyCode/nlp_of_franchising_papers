import pymupdf as fitz
from src.config import ReaderConfig
from typing import Optional, Generator, Tuple
from src.pdf_reader.page import PaperPage
import logging
logger = logging.getLogger("WFM.PdfReader")


class PdfReader:
    """
    A PDF Reader class that manages PDF operations and provides a generator to iterate through pages.
    """

    def __init__(self, conf: ReaderConfig):
        """
        Initialize the PdfReader
        """
        self.config = conf
        self.doc: Optional[fitz.Document] = None
        logger.info("PdfReader initialized")

    def set_config(self, **kwargs):
        """
        Update the ReaderConfig with a new configuration dictionary.
        """
        self.config.set_config(kwargs["path"])
        logger.debug("PdfReader config set")

    def open(self):
        """
        Open the PDF file specified in the configuration.

        :raises ValueError: If the path is not set in the configuration.
        :raises FileNotFoundError: If the specified PDF file does not exist.
        :raises Exception: For other errors during opening the PDF.
        """
        path = self.config.get("path")
        logger.debug(f"Opening file: {path}")
        if not path:

            raise ValueError("PDF path is not set in the configuration.")
        try:
            self.doc = fitz.open(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at path '{path}' was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while opening the PDF: {e}")

    def close(self):
        """
        Close the currently opened PDF file.

        :raises ValueError: If no PDF is currently opened.
        """
        if self.doc:
            self.doc.close()
            logger.debug("PdfReader closed")
            self.doc = None
        else:
            raise ValueError("No PDF file is currently opened.")

    def read(self) -> Generator[Tuple[int, PaperPage], None, None]:
        """
        Generator to iterate through the pages of the PDF.

        :yield: A tuple containing the page number (1-based) and a PaperPage object.
        :raises ValueError: If the PDF is not opened.
        """
        if not self.doc:
            raise ValueError("PDF file is not opened. Call the 'open' method first.")

        for page_num in range(self.doc.page_count):
            try:
                fitz_page = self.doc.load_page(page_num)
                paper_page = PaperPage(fitz_page)
                yield page_num + 1, paper_page
            except Exception as e:
                logger.warning(f"An error occurred while reading the page {page_num+1}: {e}")

    def __len__(self):
        if self.doc:
            return len(self.doc)
        return 0

    def __enter__(self):
        """
        Enable usage of PdfReader with the 'with' statement.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensure the PDF is closed when exiting the 'with' block.
        """
        if self.doc:
            self.close()




