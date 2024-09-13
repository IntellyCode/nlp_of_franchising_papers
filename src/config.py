import logging
from abc import ABC, abstractmethod
from typing import Optional
logger = logging.getLogger("RS.Config")


class Config(ABC):
    """
    Abstract base class for configuration settings.

    Attributes:
        _config (dict): A dictionary to store configuration settings.
                        This dictionary is meant to be populated in derived classes
                        with configuration parameters specific to their functionality.
    """

    def __init__(self):
        logger.debug("Config Initialized")
        self._config = {}

    def get_config(self):
        """
        Abstract method to get the configuration.

        Returns:
            dict: The configuration dictionary.
        """
        return self._config

    @abstractmethod
    def set_config(self, config: dict):
        """
        Abstract method to set the configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        pass

    def get(self, key):
        """
        Retrieve a configuration value by key.

        Args:
            key (str): The key for the configuration value.

        Returns:
            The value associated with the given key, or None if the key does not exist.
        """
        return self._config.get(key)


class ReaderConfig(Config):
    def __init__(self):
        super().__init__()
        self._config = {
            "path": None,
        }

    def set_config(self, path: Optional[str] = None):
        if path:
            self._config["path"] = path
            return
        raise KeyError("Path key not found in the configuration.")

    def get_path(self) -> Optional[str]:
        return self._config.get("path")
