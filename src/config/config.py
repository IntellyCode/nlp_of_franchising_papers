import logging
from abc import ABC, abstractmethod
logger = logging.getLogger("WFM.Config")


class Config(ABC):
    """
    Abstract base class for configuration settings.

    Attributes:
        _config (dict): A dictionary to store configuration settings.
                        This dictionary is meant to be populated in derived classes
                        with configuration parameters specific to their functionality.
    """

    def __init__(self):
        logger.info("Config Initialized")
        self._config = {}

    def get(self, key):
        """
        Retrieve a configuration value by key.

        Args:
            key (str): The key for the configuration value.

        Returns:
            The value associated with the given key, or None if the key does not exist.
        """
        logger.debug(f"Getting configuration value by key: {key}")
        return self._config.get(key)
