from typing import Optional
from src.config import ReaderConfig, ProcessorConfig, LdaConfig
from src.processor import Processor, Lda
from src.pdf_reader import PdfReader


class App:
    def __init__(self, gui, gui_data):
        # Initialize configurations and components
        self._reader_config = ReaderConfig()
        self._reader = PdfReader(self._reader_config)

        self._processor_config = ProcessorConfig()
        self._processor_config.set_config(capitalise=False)
        self._processor = Processor(self._processor_config, 'en_core_web_sm')

        self._lda_config = LdaConfig()
        self._lda_config.set_config(**gui_data[0])
        self._lda = Lda(self._lda_config)

        self.gui = gui
        self.gui_data = gui_data

    def start_processing(self, output_path: str):
        if not self.gui_data[1]:
            self.gui.show_error("No Files Selected!")
            return

        list_length = len(self.gui_data[1])
        for index, tup in enumerate(self.gui_data[1]):
            _, file_path = tup
            text = self.process_file(file_path)
            if not text:
                continue

            # Process the text and add to the LDA model
            self._processor.set_text(text)
            self._lda.append_to_dtm(self._processor.process())
            progress = index / list_length * 100
            self.gui.update_bar(progress)

        # Train and visualize the LDA model
        try:
            self._lda.train_model()
            self._lda.visualise(output_path)
        except Exception as e:
            self.gui.show_error("There was an error with the model: " + str(e))

    def process_file(self, file_path) -> Optional[str]:
        # Set file path and open the reader
        self._reader.set_path(file_path)
        try:
            self._reader.open()
        except ValueError as e:
            self.gui.show_error("There is a value error: " + str(e))
            return None
        except FileNotFoundError as e:
            self.gui.show_error("Where is the file?" + str(e))
            return None
        except Exception as e:
            self.gui.show_error("Something went wrong: " + str(e))
            return None

        # Read and return text from PDF
        text = ""
        for page_num, page in self._reader.read():
            text += page.get_text()
        return text
