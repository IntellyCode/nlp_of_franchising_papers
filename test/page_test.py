import fitz

config = {
    "path": "../data/ISOF 2003_Table of Contents_unlocked.pdf",
    "title_pages": [4, 32, 61, 87, 89, 108, 133, 160, 188, 204, 224, 243, 262, 269, 278, 286, 315, 336, 364, 383, 398, 419, 449, 468, 491, 513, 536]
}

doc = fitz.open(config.get("path"))
page = doc[53]
page_blocks = page.get_text("dict")["blocks"]
for block in page_blocks:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                print(span)
                if "bold" in span["font"].lower():
                    print("Is Bold")
                else:
                    print("Not Bold")
