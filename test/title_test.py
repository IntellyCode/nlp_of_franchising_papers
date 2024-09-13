import fitz

config = {
    "path": "../data/ISOF 2003_Table of Contents_unlocked.pdf",
    "title_pages": [4, 32, 61, 87, 89, 108, 133, 160, 188, 204, 224, 243, 262, 269, 278, 286, 315, 336, 364, 383, 398, 419, 449, 468, 491, 513, 536]
}

doc = fitz.open(config.get("path"))
title_pages=[]
for i in range(len(doc)):
    count = 0
    has_bold = False
    no_dot = True
    has_images = False
    is_figure = False
    page = doc[i]
    blocks = page.get_text("dict")['blocks']
    image_list = page.get_images(full=True)
    if image_list:
        # print(image_list)
        has_images = True
    for block in blocks:
        if 'lines' in block:
            for line in block['lines']:
                for span in line['spans']:
                    if bool(span["text"].strip()):
                        text = span["text"].lower()
                        if any(keyword in text for keyword in
                            ("presented","isof")) and "conference" in text:
                            if i+1 not in title_pages:
                                title_pages.append(i+1)

                        """
                        
                        
                        if any(keyword in text for keyword in
                               ("figure", "table","abstract","keywords","summary","introduction","appendix","references","annex","conclusion")):
                            is_figure = True
                        if "bold" in span["font"].lower():
                            has_bold = True
                            if text.endswith("."):
                                no_dot = False
                        count+= len(span["text"].split(" "))
                        """

    #if count <= 200 and has_bold and no_dot and not has_images and not is_figure:
     #   title_pages.append(i+1)


print(title_pages)
print(title_pages==config.get("title_pages"))

# [1, 34, 38, 70, 114, 115, 147, 156, 177, 181, 193, 212, 213, 214, 215, 220, 253, 275, 301, 313, 314, 343, 382, 406, 430, 443, 493, 529, 559, 577, 581, 616, 649, 674, 679, 688, 707, 738, 755, 767, 789, 826, 850, 852, 853, 869, 870, 871, 873, 874, 875, 876, 877, 878, 879, 890, 891, 905, 906, 924, 971, 995, 1001, 1002, 1042, 1066, 1108, 1133, 1151, 1155]
