import logging
from abc import ABC, abstractmethod
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
            "pages": (None, None)
        }

    def set_config(self, config: dict):
        if "path" in config and "pages" in config:
            self._config["path"] = config["path"]
            self._config["pages"] = config["pages"]
            return
        raise KeyError("Path or page keys not found.")


class PlotterConfig(Config):
    """
    Configuration class for Plotter settings.

    Attributes:
        _config (dict): A dictionary containing plotter-specific configuration settings, including:
            - "plot_size" (tuple): The size of the plots (width, height).
            - "scatter_size" (tuple): The size of the scatter plots (width, height).
            - "show" (bool): Whether to display the plots.
            - "path" (str, optional): The file path for saving plot images.
            - "colormap" (str, optional): The desired Matplotlib colormap.
    """

    def __init__(self):
        super().__init__()
        self._config = {
            "figsize": (10,10),
            "path": None,
            "show": True,
            "colormap": "viridis"
        }

    def set_config(self, figsize=None, show=None, path=None, colormap=None):
        """
        Sets the plotter configuration with the specified parameters.

        Args:
            figsize (tuple, optional): The size of the plots (width, height).
            show (bool, optional): Whether to show the plots.
            path (str, optional): The file path for saving plot images.
            colormap (str, optional): The desired Matplotlib colormap.
        """
        logger.debug(f"Plotter Config: {figsize}, {show}, {path}, {colormap}")
        if figsize:
            self._config["scatter_size"] = figsize
        if show is not None:
            self._config["show"] = show
        if path:
            self._config["path"] = path
        if colormap:
            self._config["colormap"] = colormap

