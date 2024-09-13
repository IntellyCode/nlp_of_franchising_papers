from src.config import ReaderConfig, PlotterConfig
from src.data_plotting import BubblePlotter

sorted_frequencies = []

plotter_config = PlotterConfig()
bp = BubblePlotter(plotter_config, len(sorted_frequencies))
bp.init_figure()
bp.set_name("2005 Papers: Most Used Words")
bp.add(sorted_frequencies)
bp.plot()
