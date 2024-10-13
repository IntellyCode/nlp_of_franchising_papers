import tkinter as tk
from typing import Optional


class InputField:
    """
    Class representing an input field with a label.

    :param parent: The parent widget.
    :param label_text: The text for the label.
    :param default_value: The default value for the input field.
    """

    def __init__(self, parent: tk.Widget, label_text: str, default_value: Optional[str] = '') -> None:

        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, expand=True)

        self.label = tk.Label(frame, text=label_text,width=10)
        self.entry = tk.Entry(frame)
        self.entry.insert(0, default_value)
        self.label.pack(side=tk.LEFT,anchor='w')
        self.entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

    def get_value(self) -> str:
        """
        Get the current value of the input field.

        :return: The input field value.
        """
        return self.entry.get()

    def set_value(self, value: str) -> None:
        """
        Set the value of the input field.

        :param value: The value to set.
        :return: None
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def get_entry(self):
        return self.entry
