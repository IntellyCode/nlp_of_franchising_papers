from src.config import *
from src.text_extractor import PdfReader
from src.text_processor import Processor
from src.lat_dir_all import LatDirAll
import pyLDAvis.gensim_models
config = ReaderConfig()
config.set_config("./data/2004 ISOF Conference Papers.pdf")
reader = PdfReader(config)
reader.open()
texts = []
text = ""
for page_num, page in reader.read():
    text += page.get_text()
    if page_num % 50 == 0:
        print("On Page:", page_num)
        texts.append(text)
        text = ""
if text != "":
    texts.append(text)

conf = ProcessorConfig()
conf.set_config({"capitalise": False})
processor = Processor(conf, 'en_core_web_sm')

conf = LdaConfig()
conf.set_config({"alpha":0.1, "beta":0.3})
lat_dir_all = LatDirAll(conf)
for text in texts:
    processor.set_text(text)
    lat_dir_all.append_to_dtm(processor.process())

lat_dir_all.train_model()

vis = pyLDAvis.gensim_models.prepare(lat_dir_all.get_model(), lat_dir_all.get_corpus(), lat_dir_all.get_dictionary())
pyLDAvis.save_html(vis, 'lda_visualization.html')
print("LDA visualization saved as 'lda_visualization.html'")