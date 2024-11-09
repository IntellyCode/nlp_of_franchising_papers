import unittest
import pymupdf as fitz
from src.pdf_reader import PaperPage, PdfReader
from src.config import ReaderConfig
from unittest.mock import MagicMock
from src.config import special_character


class TestPaperPage(unittest.TestCase):

    def setUp(self):

        self.reader = PdfReader(ReaderConfig())
        self.reader.set_path("../data/2022 Test 4.pdf")
        self.reader.open()

    def test_get_text(self):
        self.reader.probe()
        text = self.reader.read()
        print(text)

    def test_probe(self):
        self.reader.probe()

if __name__ == "__main__":
    unittest.main()
