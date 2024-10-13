from src.gui.pane import Pane
import tkinter as tk
from typing import Callable, List


class ActionPane(Pane):
    """
    Pane that contains action buttons.

    :param parent: The parent widget.
    :param actions: A list of dictionaries specifying action button configurations.
    :param **kwargs: Additional keyword arguments for Pane.
    """

    def __init__(self, parent: tk.Widget, actions: List[dict], **kwargs) -> None:
        super().__init__(parent, **kwargs)
        for action in actions:
            button = tk.Button(self.frame, text=action.get('text', 'Button'), command=action.get('command'))
            button.pack(side=tk.LEFT, padx=5, pady=5)
