from src.config import Config


class GuiConfig(Config):
    def set_config(self,
                   hidden_directories: bool = False):
        self._config = {
            "hidden_directories": hidden_directories
        }