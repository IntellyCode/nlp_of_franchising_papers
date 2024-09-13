from src.config import ReaderConfig, PlotterConfig
from src.bag_of_words import BagOfWords
from src.data_plotting import BubblePlotter
from src.text_extractor import Reader
from src.text_processor import Processor

config = {
        "path": "./data/2005 ISOF Cpnference Papers.pdf",
        "title_pages": [1,38, 70, 115, ]
    }
reader_config = ReaderConfig()
reader_config.set_config(config)

reader = Reader(reader_config)
text = reader.read_papers()

processor = Processor()
tags = ["ADP","AUX","CCONJ","DET","INTJ","NUM","PART","PRON","PUNCT","SCONJ","SYM","X"]
filtered_text = processor.exclude_tokens_by_pos(text, tags)
bow = BagOfWords(filtered_text)
frequencies = bow.extract_frequencies()
sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
print(sorted_frequencies)
"""
sorted_frequencies = [item for item in sorted_frequencies if item[0] != "-"]

first_four = sorted_frequencies[:4]
s = 0
for _, f in first_four:
    s += f

sorted_frequencies = [("franchise", s)] + sorted_frequencies[4:20]
"""

