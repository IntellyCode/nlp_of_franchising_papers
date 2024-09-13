import fitz
import re
config = {
    "path": "../data/ISOF 2003_Table of Contents_unlocked.pdf",
    "title_pages": [4, 32, 61, 87, 89, 108, 133, 160, 188, 204, 224, 243, 262, 269, 278, 286, 315, 336, 364, 383, 398, 419, 449, 468, 491, 513, 536]
}


def is_bold(span):
    return "bold" in span['font'].lower()


def find_reference_pages(pdf_path):
    reference_pages = []
    reference_last_pages =[]
    reading_references = False
    doc = fitz.open(pdf_path)
    references_pattern = re.compile(r"\b(references|resources)[\s\W]*$", re.IGNORECASE)
    for i in range(doc.page_count):
        new_page = True
        page = doc.load_page(i)
        page_blocks = page.get_text("dict")["blocks"]

        # Iterate through blocks of text on the page
        for block in page_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span['text'].lower()
                        if is_bold(span) and references_pattern.search(text) and not reading_references:
                            reading_references = True
                            new_page = False

                        if is_bold(span) and reading_references and new_page:
                            reading_references = False
                            if i+1 not in reference_last_pages:
                                reference_last_pages.append(i+1)

                        if reading_references:
                            if i+1 not in reference_pages:
                                reference_pages.append(i+1)

    doc.close()
    print(reference_last_pages)
    reference_pages = [page for page in reference_pages if page not in reference_last_pages]
    return reference_pages


references = find_reference_pages(config["path"])
print("Reference Pages:", references)
