from src.config import *
from src.pdf_reader.text_extractor import PdfReader
from src.processor.text_processor import Processor
from src.processor.lda import Lda
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

config = ReaderConfig()
config.set_config("./data/2004 ISOF Conference Papers.pdf")
reader = PdfReader(config)
reader.open()
texts = []
text = ""
for page_num, page in reader.read():
    text += page.get_text()
    if page_num % 50 == 0:
        texts.append(text)
        text = ""
if text != "":
    texts.append(text)

conf = ProcessorConfig()
conf.set_config(capitalise=False)
processor = Processor(conf, 'en_core_web_sm')

conf = LdaConfig()
conf.set_config()
lat_dir_all = Lda(conf)
for text in texts:
    processor.set_text(text)
    lat_dir_all.append_to_dtm(processor.process())

lat_dir_all.train_model()

lat_dir_all.visualise("lda_visualization.html")
