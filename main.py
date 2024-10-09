from src.config import ReaderConfig, PlotterConfig
from src.data_plotting import BubblePlotter
from src.text_extractor import PdfReader
from src.text_processor import Processor
from src.keywords import business_terms

paths = ["./data/2004 ISOF Conference Papers.pdf"]
processor = Processor()
tags = ["ADP", "AUX", "CCONJ", "DET", "INTJ", "NUM", "PART", "PRON", "PUNCT", "SCONJ", "SYM", "X"]
keywords = business_terms
matcher = processor.create_matcher(keywords)
for path in paths:
    print(path)
    reader_config = ReaderConfig()
    reader_config.set_config(path=path)

    reader = PdfReader(reader_config)
    try:
        reader.open()
    except Exception as e:
        print(e)
        continue
    terms = {

    }
    page_count = len(reader)
    for page_num, page in reader.read():
        # print(f"Progress: {round(page_num/page_count*100)}")
        filtered_text = processor.exclude_tokens_by_pos(page.get_text(), tags)
        terms = processor.extract_keywords(filtered_text, matcher,terms)

    reader.close()
    sorted_frequencies = sorted(terms.items(), key=lambda x: x[1], reverse=True)
    print(sorted_frequencies[0:100])
