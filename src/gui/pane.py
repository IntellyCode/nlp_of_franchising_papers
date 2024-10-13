import tkinter as tk
from typing import Optional


class Pane:
    """
    Base class for panes in the GUI.

    :param parent: The parent widget.
    :param width: The width of the pane.
    :param height: The height of the pane.
    :param **kwargs: Additional keyword arguments for customization.
    """

    def __init__(self, parent: tk.Widget, width: Optional[int] = None, height: Optional[int] = None, **kwargs) -> None:
        self.frame = tk.Frame(parent, width=width, height=height, **kwargs)
        if width or height:
            self.frame.pack_propagate(False)  # Prevent frame from resizing to fit contents

    def get_frame(self) -> tk.Frame:
        """
        Get the Tkinter Frame associated with this pane.

        :return: The frame widget.
        """
        return self.frame
