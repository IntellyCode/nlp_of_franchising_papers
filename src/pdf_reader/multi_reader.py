from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import unittest
import os
from src.config import ReaderConfig

from src.pdf_reader import PdfReader

logger = logging.getLogger("WFM.MultiReader")


class MultiReader:
    """
    A multi-threaded PDF reader that processes multiple PDF files concurrently.
    """

    def __init__(self, directory: str, config: ReaderConfig):
        self.directory = directory
        self.config = config
        self.pdf_files = self._get_pdf_files(directory)
        self.texts: List[Optional[str]] = [None] * len(self.pdf_files)  # Placeholder for storing the texts in correct order

    def _get_pdf_files(self, directory: str):
        """
        Get a sorted list of PDF files from the specified directory.
        """
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        pdf_files.sort()  # Sort files alphabetically
        return pdf_files

    def _read_pdf(self, pdf_path: str, index: int):
        """
        Helper function to read a single PDF and store the result at the correct index.
        """
        pdf_reader = PdfReader(self.config)
        pdf_reader.set_path(pdf_path)
        try:
            pdf_reader.open()
            text = pdf_reader.read()
            pdf_reader.close()
            logger.info(f"Successfully read {pdf_path}")
        except Exception as e:
            logger.warning(f"Error reading {pdf_path}: {e}")
            text = ""
        self.texts[index] = text

    def read_all(self):
        """
        Read all PDFs in the directory concurrently and return the texts in the correct order.
        """
        with ThreadPoolExecutor() as executor:
            futures = []
            for index, pdf_file in enumerate(self.pdf_files):
                pdf_path = os.path.join(self.directory, pdf_file)
                futures.append(executor.submit(self._read_pdf, pdf_path, index))

            for future in as_completed(futures):
                future.result()

        return self.texts


class TestMultiReader(unittest.TestCase):
    def setUp(self):
        # Create a test data directory if it doesn't exist
        self.test_directory = "../../data"
        logger.setLevel(logging.DEBUG)

    def test_read_all_pdfs(self):
        # Set up MultiReader with the test directory and a dummy config
        config = ReaderConfig()
        multi_reader = MultiReader(self.test_directory, config)

        # Perform the read_all operation
        results = multi_reader.read_all()

        print(len(results))


    def test_read_with_errors(self):
        # Introduce an error by removing one file before reading
        os.remove(os.path.join(self.test_directory, "Paper 2.pdf"))

        # Set up MultiReader with the test directory and a dummy config
        config = ReaderConfig()
        multi_reader = MultiReader(self.test_directory, config)

        # Perform the read_all operation
        results = multi_reader.read_all()

        print(len(results))

if __name__ == "__main__":
    unittest.main()
