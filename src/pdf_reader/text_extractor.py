import pymupdf as fitz
from src.config import ReaderConfig
from src.pdf_reader.page import PaperPage
from collections import defaultdict
import logging

logger = logging.getLogger("WFM.PdfReader")


class PdfReader:
    """
    Manages PDF operations and provides a generator to iterate through pages.
    """

    def __init__(self, config: ReaderConfig):
        self._config = config
        self._doc = None
        self._common_fonts = {}
        logger.info("PdfReader initialized")

    def _populate_common_fonts(self, data):
        max_num_key = None
        max_num_value = float('-inf')

        max_str_key = None
        max_str_value = float('-inf')

        for key, value in data.items():
            try:
                float_key = float(key)
                if value > max_num_value:
                    max_num_key = float_key
                    max_num_value = value
            except ValueError:
                if value > max_str_value:
                    max_str_key = key
                    max_str_value = value
        self._common_fonts["fontsize"] = max_num_key
        self._common_fonts["fonttype"] = max_str_key

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

    def probe(self):
        """
        Function to probe pages 2, 3 and 4 to identify most common font size and font type

        :return: (int, str): font size, font type
        """
        logger.info("Probing Pdf")
        self._ensure_document_open()
        page_1 = PaperPage(self._doc.load_page(1)).get_font()
        page_2 = PaperPage(self._doc.load_page(2)).get_font()
        page_3 = PaperPage(self._doc.load_page(3)).get_font()

        result = defaultdict(int)

        for d in [page_1, page_2, page_3]:
            for key, value in d.items():
                result[key] += value
        self._populate_common_fonts(result)

    def read(self) -> str:
        """
        Function to read the entire pdf with or without references
        :return: (str) Pdf text
        """
        self._ensure_document_open()
        text = ""
        skip = False
        for page_num in range(self._doc.page_count):
            if skip:
                logger.debug(f"Skipping page {page_num}")
                continue
            try:
                page = PaperPage(self._doc.load_page(page_num))
                found_references, string = page.get_text(find_references=True,
                                                         fontsize=self._common_fonts.get("fontsize"),
                                                         fonttype=self._common_fonts.get("fonttype"))
                logger.debug(f"Extracted string: {string}")
                if found_references:
                    logger.debug("Found References")
                    skip = True
                text += string
            except Exception as e:
                logger.warning(f"Error reading page {page_num + 1}: {e}")
        return text

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
