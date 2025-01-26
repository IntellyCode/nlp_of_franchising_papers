from .pane import Pane
from .input_field import InputField
import tkinter as tk
from typing import List


class ConfigPane(Pane):
    """
    Configuration pane that includes multiple input fields.

    :param parent: The parent widget.
    :param inputs: A list of dictionaries specifying input field configurations.

    :param **kwargs: Additional keyword arguments for Pane.
    """

    def __init__(self, parent: tk.Widget, inputs: List[dict], **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.input_fields = []
        for input_config in inputs:
            input_field = InputField(self.frame, input_config.get('label', ''), input_config.get('default', ''))
            self.input_fields.append(input_field)

    def get_values(self) -> dict:
        """
        Get the values from all input fields.

        :return: A dictionary of input field values.
        """
        return {field.label['text']: field.get_value() for field in self.input_fields}
