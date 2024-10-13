import tkinter as tk
from typing import Optional

from .pane import Pane
from tkinter import ttk


class ProgressBar(Pane):
    """
    Circular ProgressBar Pane that visually represents progress.

    :param parent: The parent widget.
    :param diameter: Diameter of the progress bar.
    :param **kwargs: Additional keyword arguments for Pane.
    """

    def __init__(self, parent: tk.Widget, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._progressbar = ttk.Progressbar(master=parent, length=600,value=0)
        self._progressbar.pack(side=tk.LEFT, fill=tk.X, expand=False)

    def update(self, progress: float) -> Optional[float]:
        """
        Update the progress display based on the provided progress value.

        :param progress: Float between 0 and 1 representing the progress level.
        :return: None
        """
        if progress < 0 or progress > 100:
            return progress
        if progress + self._progressbar['value'] >= 100:
            self._progressbar['value'] = 100
        else:
            self._progressbar.step(progress)

    def clear(self):
        self._progressbar['value'] = 0
