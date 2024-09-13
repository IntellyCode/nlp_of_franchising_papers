import pymupdf as fitz
from typing import List, Any, Generator


class PaperPage:
    """
    A custom Page class that wraps around the fitz.Page object.
    Provides additional methods or properties as needed.
    """

    def __init__(self, fitz_page: fitz.Page):
        self._fitz_page = fitz_page

    @staticmethod
    def _loop(blocks: List, depth: int) -> Generator[Any, Any, Any]:
        """
        A private generator method to traverse the nested structure of the page's text blocks.

        :param blocks: A list of blocks from the page's text dictionary.
        :param depth: The target depth to extract elements from (0 to 2).
                      0: Blocks
                      1: Lines within blocks
                      2: Spans within lines
        :return: A generator yielding elements at the specified depth.
        :raises ValueError: If the depth is not between 0 and 2.
        """
        if depth < 0 or depth > 2:
            raise ValueError("Depth must be between 0 and 2.")

        for block in blocks:
            if block['type'] != 0:  # Only process text blocks
                continue
            if depth == 0:
                yield block
            for line in block.get("lines", []):
                if depth == 1:
                    yield line
                for span in line.get("spans", []):
                    if depth == 2:
                        yield span

    def get_text(self, **kwargs):
        """
        Extract text from the page.
        You can pass fitz.Page.get_text() parameters via kwargs.
        """
        return self._fitz_page.get_text(**kwargs)

    def get_image_list(self):
        """
        Retrieve a list of images on the page.
        """
        return self._fitz_page.get_images()

    def get_bold_text(self) -> List[str]:
        """
        Extract and return all bold text from the page.

        Returns:
            List[str]: A list of bold text strings found on the page.
        """
        bold_texts = []
        blocks = self._fitz_page.get_text("dict")["blocks"]

        for span in PaperPage._loop(blocks, 2):
            text = span.get("text", "").strip()
            if not text:
                continue
            font_name = span.get("font", "").lower()
            if "bold" in font_name:
                bold_texts.append(text)
        return bold_texts

    def get_tables(self, **kwargs) -> List[dict]:
        return self._fitz_page.find_tables(**kwargs)

    def get_fonts(self, **kwargs) -> List:
        return self._fitz_page.get_fonts(**kwargs)


if __name__ == '__main__':
    doc = fitz.open("../data/2004 ISOF Conference Papers.pdf")
    page = PaperPage(doc.load_page(50))
    print(page.get_text())
    print(page.get_fonts())
