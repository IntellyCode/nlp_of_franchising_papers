import threading
from os import path
from src.gui import Gui
from src.config import Config
from .app import App
import logging
from datetime import datetime
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger("WFM.Controller")


class _Thread(threading.Thread):
    def __init__(self, app_instance, output_path: str):
        super().__init__()
        self.app_instance = app_instance
        self.output_path = output_path

    def run(self):
        # Run the App instance's start function in this thread
        self.app_instance.start_processing(self.output_path)


class Controller:
    def __init__(self, conf: Config):
        self._config = conf
        self._gui_data = ()
        self.thread_pool = []  # Store all thread instances

        # Initialize GUI with start callback
        self._gui = Gui(self.start)
        self._gui.run()

    def start(self):
        # Start a new App instance and thread each time this is called
        self._gui_data = self._gui.get_data()
        output_dict = self._gui_data[2]
        _ = output_dict.get('viewing_dir').split(path.sep)[-1]
        logger.debug(f"Viewing Directory: {_}")
        file_name = f"{_}_lda_visualization_{datetime.now()}.html"
        output_dir = output_dict.get("output_dir")
        if not output_dir:
            self._gui.show_error("Enter output directory")
            return

        output_path = path.join(output_dir, file_name)
        self._gui.update_bar(-1)

        # Create a new App instance and thread for this start action
        app_instance = App(self._gui, self._gui_data)
        thread = _Thread(app_instance, output_path)
        self.thread_pool.append(thread)  # Keep track of threads
        thread.start()



if __name__ == '__main__':
    c = Controller(Config())
