from src.config import Config
from typing import Optional


class ReaderConfig(Config):
    def set_config(self, path: str):
        """
        :param path: Path to file
        :return:
        """
        if path:
            self._config["path"] = path
            return
        raise KeyError("Path key not found in the configuration.")

