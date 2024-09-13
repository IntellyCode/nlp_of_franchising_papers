from src.config import PlotterConfig
import matplotlib.pyplot as plt
import numpy as np
import logging
import math
from typing import List, Tuple
from src.util import compress_linear
from PIL import ImageFont
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
            max_font_size (float, optional): The maximum font size. Default is 45

        Returns:
            float: The computed font size.
        """

        # Use a quadratic function to calculate font size
        font_size = (radius ** 1.5)

        # Ensure font size is within the defined bounds
        font_size = max(min_font_size, min(font_size, max_font_size))

        return font_size

    @staticmethod
    def _calc_angle(radius):
        return max(12, min(radius*8, 45))

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
    l = [('nlp', 17), ('language', 12), ('text', 10), ('models', 7), ('human', 6), ('recognition', 6), ('learning', 5), ('tasks', 5), ('such', 5), ('words', 5), ('natural', 4), ('machine', 4), ('understand', 3), ('deep', 3), ('sentiment', 3), ('analysis', 3), ('speech', 3), ('particularly', 3), ('challenges', 3), ('many', 3), ('applications', 3), ('significant', 3), ('more', 3), ('data', 3), ('systems', 3), ('processing', 2), ('focuses', 2), ('computers', 2), ('humans', 2), ('goal', 2), ('useful', 2), ('field', 2), ('methods', 2), ('classification', 2), ('translation', 2), ('named', 2), ('entity', 2), ('categories', 2), ('used', 2), ('spam', 2), ('other', 2), ('customer', 2), ('key', 2), ('multiple', 2), ('context', 2), ('different', 2), ('people', 2), ('including', 2), ('input', 2), ('better', 2), ('understanding', 2), ('generation', 2), ('ner', 2), ('involves', 2), ('time', 2), ('research', 2), ('various', 2), ('virtual', 2), ('assistants', 2), ('conversational', 2), ('ai', 2), ('building', 2), ('dialogue', 2), ('chatbots', 2), ('need', 2), ('tokenization', 2), ('stemming', 2), ('lemmatization', 2), ('steps', 2), ('further', 2), ('form', 2), ('making', 2), ('advancements', 2), ('still', 2), ('challenge', 2), ('training', 2), ('vast', 2), ('subfield', 1), ('artificial', 1), ('intelligence', 1), ('interaction', 1), ('ultimate', 1), ('enable', 1), ('interpret', 1), ('respond', 1), ('way', 1), ('meaningful', 1), ('combines', 1), ('computational', 1), ('linguistics', 1), ('structure', 1), ('statistical', 1), ('encompasses', 1), ('several', 1), ('important', 1), ('others', 1), ('example', 1), ('process', 1), ('assigning', 1), ('labels', 1), ('based', 1), ('content', 1), ('widely', 1), ('email', 1), ('filtering', 1), ('emails', 1), ('automatically', 1), ('categorized', 1), ('hand', 1), ('determine', 1), ('emotion', 1), ('expressed', 1), ('piece', 1), ('monitoring', 1), ('social', 1), ('media', 1), ('feedback', 1), ('dealing', 1), ('ambiguity', 1), ('variability', 1), ('have', 1), ('meanings', 1), ('depending', 1), ('express', 1), ('same', 1), ('idea', 1), ('numerous', 1), ('ways', 1), ('makes', 1), ('difficult', 1), ('system', 1), ('only', 1), ('literal', 1), ('meaning', 1), ('also', 1), ('capture', 1), ('nuances', 1), ('original', 1), ('message', 1), ('modern', 1), ('techniques', 1), ('rely', 1), ('heavily', 1), ('neural', 1), ('networks', 1), ('shown', 1), ('perform', 1), ('exceptionally', 1), ('well', 1), ('variety', 1), ('transformers', 1), ('famous', 1), ('bert', 1), ('gpt', 1), ('set', 1), ('new', 1), ('benchmarks', 1), ('use', 1), ('attention', 1), ('mechanisms', 1), ('allow', 1), ('weigh', 1), ('importance', 1), ('parts', 1), ('leading', 1), ('aspect', 1), ('identifying', 1), ('classifying', 1), ('elements', 1), ('predefined', 1), ('names', 1), ('organizations', 1), ('locations', 1), ('expressions', 1), ('quantities', 1), ('monetary', 1), ('values', 1), ('percentages', 1), ('crucial', 1), ('information', 1), ('extraction', 1), ('specific', 1), ('needs', 1), ('pulled', 1), ('large', 1), ('volumes', 1), ('legal', 1), ('documents', 1), ('papers', 1), ('converts', 1), ('spoken', 1), ('critical', 1), ('component', 1), ('powers', 1), ('siri', 1), ('alexa', 1), ('dictation', 1), ('software', 1), ('transcription', 1), ('services', 1), ('achieving', 1), ('high', 1), ('accuracy', 1), ('challenging', 1), ('factors', 1), ('accents', 1), ('pronunciation', 1), ('variations', 1), ('background', 1), ('noise', 1), ('homophones', 1), ('emerging', 1), ('area', 1), ('carry', 1), ('prime', 1), ('examples', 1), ('user', 1), ('inputs', 1), ('maintain', 1), ('exchanges', 1), ('generate', 1), ('appropriate', 1), ('responses', 1), ('leverage', 1), ('intent', 1), ('management', 1), ('simulate', 1), ('like', 1), ('conversation', 1), ('fundamental', 1), ('preprocessing', 1), ('breaking', 1), ('individual', 1), ('phrases', 1), ('blocks', 1), ('reduces', 1), ('root', 1), ('goes', 1), ('step', 1), ('reducing', 1), ('base', 1), ('dictionary', 1), ('help', 1), ('standardize', 1), ('easier', 1), ('learn', 1), ('faces', 1), ('major', 1), ('bias', 1), ('lead', 1), ('biased', 1), ('produce', 1), ('unfair', 1), ('prejudiced', 1), ('outcomes', 1), ('amounts', 1), ('labeled', 1), ('supervised', 1), ('expensive', 1), ('consuming', 1), ('obtain', 1), ('additionally', 1), ('diversity', 1), ('poses', 1), ('hurdle', 1), ('most', 1), ('tools', 1), ('centered', 1), ('english', 1), ('leaving', 1), ('languages', 1), ('underrepresented', 1), ('continues', 1), ('evolve', 1), ('likely', 1), ('become', 1), ('even', 1), ('integrated', 1), ('daily', 1), ('lives', 1), ('improving', 1), ('service', 1), ('assisting', 1), ('medical', 1), ('diagnoses', 1), ('analyzing', 1), ('patient', 1), ('records', 1), ('potential', 1), ('varied', 1), ('researchers', 1), ('continuously', 1), ('working', 1), ('efficient', 1), ('less', 1), ('resource', 1), ('intensive', 1), ('complexities', 1), ('conclusion', 1), ('rapidly', 1), ('growing', 1), ('made', 1), ('strides', 1), ('recent', 1), ('years', 1), ('ongoing', 1), ('capabilities', 1), ('expanding', 1), ('bringing', 1), ('closer', 1), ('seamless', 1), ('computer', 1), ('communication', 1), ('however', 1), ('is', 1), ('much', 1), ('work', 1), ('done', 1), ('overcome', 1), ('ensure', 1), ('technologies', 1), ('accessible', 1), ('fair', 1), ('for', 1)]
    l = l[0:20]
    bp = BubblePlotter(plotter_config, len(l))
    bp.init_figure()
    bp.set_name("Plot")
    bp.add(l)
    bp.plot()






