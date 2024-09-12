from config import PlotterConfig
import matplotlib.pyplot as plt
import numpy as np
import logging
import math
from typing import List, Tuple
from util import compress_with_ln, compress_linear, compress_quadratic
logger = logging.getLogger("WFM.Plotter")


class Plotter:
    """
    A class for creating plots and scatter diagrams using matplotlib.

    Attributes:
        config (PlotterConfig): Configuration object containing plot settings.
        name (str): The name or title of the plot.
        _colormap: Colormap instance used for generating colors.
        _colors: Array of colors generated from the colormap.
    """

    def __init__(self, config: PlotterConfig, n_elements: int):
        """
        Initializes the Plotter with a PlotterConfig object.

        Args:
            config (PlotterConfig): Configuration object containing plot settings.
            n_elements (int): Number of distinct elements to plot.

        Raises:
            ValueError: If config is not an instance of PlotterConfig.
        """
        if not isinstance(config, PlotterConfig):
            raise ValueError("Config must be an instance of PlotterConfig.")
        self.config = config
        self.name = "Plot"
        self._colormap = plt.get_cmap(self.config.get("colormap"))
        self._colors = self._colormap(np.linspace(0, 0.8, n_elements))
        logger.debug(f"Plotter initialized with configuration:\n {self.config}")

    def set_name(self, name: str):
        """
        Sets the name or title of the plot.

        Args:
            name (str): The name or title for the plot.
        """
        self.name = name

    def init_figure(self):
        """
        Initializes a new figure with the specified size from the configuration.
        """
        plt.figure(figsize=self.config.get("figsize"))

    def plot(self):
        """
        Finalizes and displays or saves the plot.

        The plot is saved to the path specified in the configuration (if provided),
        and/or displayed based on the configuration settings.
        """
        plt.title(self.name)
        plt.grid(True)
        if self.config.get("path"):
            plt.savefig(self.config.get("path"))
        if self.config.get("show"):
            plt.show()

    def add(self, circles: np.array):
        """
        Adds data points to the plot.

        Args:
            circles (np.array): Array of radii in increasing order

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Implemented only by subclasses")

    def set_config(self, config: PlotterConfig):
        """
        Sets the configuration for the Plotter.

        Args:
            config (PlotterConfig): A configuration object containing plot settings.

        Raises:
            ValueError: If config is not an instance of PlotterConfig.
        """
        if not isinstance(config, PlotterConfig):
            raise ValueError("Config must be an instance of PlotterConfig.")
        self.config = config
        logger.debug(f"Configuration updated: {self.config}")


class BubblePlotter(Plotter):
    def __init__(self, config: PlotterConfig, n_elements,):
        """
        Initializes the BubblePlotter with word-frequency pairs and a PlotConfig object.

        Args:
            n_elements (int): Number of elements to plot
            config (PlotConfig): Configuration object containing plot settings.
        """
        super().__init__(config, n_elements)

        self.fig = None
        self.ax = None

    def init_figure(self):
        """
        Initializes a new figure with the specified size.
        """
        self.fig, self.ax = plt.subplots(figsize=self.config.get("figsize"))
        self.ax.set_aspect("equal")

    def plot(self):
        """
        Finalizes and displays or saves the plot.
        """
        if self.config.get("path"):
            plt.savefig(self.config.get("path"))
        if self.config.get("show"):
            plt.show()

    def _calc_coordinates(self, radii: List[int]):
        """
        Calculate coordinates for points on an Archimedean spiral.

        Args:
            radii (List[int]): A list of radii for each point.

        Returns:
            List[Tuple[float, float]]: A list of (x, y) coordinates.
        """
        coords = [(0, 0)]
        theta = 45
        radius = radii[0]+radii[1]
        for i in range(1,len(radii)):
            radius += radii[i]/3
            x = radius * math.cos(math.radians(theta))
            y = radius * math.sin(math.radians(theta))
            coords.append((x, y))
            theta += self._calc_angle(radii[i])
        return coords

    @staticmethod
    def _calc_font_size(radius: float, min_font_size: float = 8, max_font_size: float = 40) -> float:
        """
        Calculates an appropriate font size for text inside a circle based on the circle's radius
        using a quadratic function.

        Args:
            radius (float): The radius of the circle.
            min_font_size (float, optional): The minimum font size. Default is 8.
            max_font_size (float, optional): The maximum font size. Default is 20.

        Returns:
            float: The computed font size.
        """
        # Use a quadratic function to calculate font size
        font_size = (radius ** 1.8)

        # Ensure font size is within the defined bounds
        font_size = max(min_font_size, min(font_size, max_font_size))

        return font_size

    @staticmethod
    def _calc_angle(radius):
        return max(12, min(radius*15, 45))

    def add(self, elements: List[Tuple[str, int]]):
        """
        Adds bubble data to the plot.

        Args:
            elements (List[Tuple[str, int]]): List of word-frequency pairs.
        """
        elements = sorted(elements, key=lambda x: x[1],reverse=True)
        labels, freqs = [], []
        for l, f in elements:
            labels.append(l)
            freqs.append(f)
        radii = compress_linear(freqs)
        coords = self._calc_coordinates(radii)
        for i in range(len(labels)):
            circle = plt.Circle(
                coords[i],
                radii[i],
                color=self._colors[i],
                label=labels[i]
            )
            self.ax.add_patch(circle)
            self.ax.text(
                coords[i][0],coords[i][1],
                labels[i],
                horizontalalignment='center',
                verticalalignment='center',
                color="white",
                fontsize=self._calc_font_size(radii[i])
            )
        self.ax.axis("off")
        self.ax.relim()
        self.ax.autoscale_view()


if __name__ == "__main__":
    plotter_config = PlotterConfig()
    l = [('nlp', 17), ('language', 12), ('text', 10), ('models', 7), ('human', 6), ('recognition', 6), ('learning', 5), ('tasks', 5), ('such', 5), ('words', 5), ('natural', 4)]
    print(len(l))
    bp = BubblePlotter(plotter_config, len(l))
    bp.init_figure()
    bp.add(l)
    bp.plot()






