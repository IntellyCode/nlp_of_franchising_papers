import fitz
from config import ReaderConfig
import numpy as np


class Reader:
    def __init__(self, config: ReaderConfig):
        self.config = config
        self.doc = fitz.open(self.config.get("path"))

    @staticmethod
    def _is_not_only_space(s: str) -> bool:
        """
        Checks if the string is not only composed of whitespace characters.
        """
        return bool(s.strip())

    def _read_paper(self, start: int, end: int) -> str:
        """
        Reads text from pages in the PDF from 'start' to 'end',
        appending only non-bold text to a common string. Stops
        when 'references' is found in the text.

        Args:
            start (int): The start page number (0-indexed).
            end (int): The end page number (exclusive).

        Returns:
            str: A string containing all non-bold text from the specified page range.
        """
        text = ""

        for page_num in range(start, end):
            page = self.doc[page_num]
            blocks = page.get_text("dict")['blocks']

            for block in blocks:
                if 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            if "references" in span['text'].lower():
                                return text.lower()
                            if "bold" in span['font'].lower():
                                continue
                            if self._is_not_only_space(span["text"]):
                                text += span['text'] + " "

        return text.lower()

    def read_papers(self):
        text = " "
        title_pages = np.array(self.config.get("title_pages"))
        title_pages = title_pages - 1
        for i in range(1, len(title_pages)):
            if title_pages[i-1] < 0 or title_pages[i] < 0:
                continue
            # noinspection PyTypeChecker
            text += self._read_paper(title_pages[i-1]+1,  title_pages[i]-1) + " \n"
        return text


if __name__ == "__main__":
    config = {
        "path": "../data/2004 ISOF Conference Papers.pdf",
        "title_pages": [3, 29, 61, 83, 113, 145, 183, 216, 233, 266, 290, 324, 350, 366, 389, 419, 451, 482, 507, 544]
    }
    reader_config = ReaderConfig()
    reader_config.set_config(config)

    reader = Reader(reader_config)
    print(reader.read_papers())

