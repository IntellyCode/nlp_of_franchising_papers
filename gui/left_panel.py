from gui.panel import Panel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import os
from .scrollable import ScrollableList
import numpy as np


class LeftPanel(Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.open_path = os.path.expanduser("~")
        sl = ScrollableList(self.get_dirs())
        self.layout().addWidget(sl)

    def set_path(self, path: str):
        if not os.path.exists(path):
            raise ValueError(f"The path '{path}' does not exist.")
        if not os.path.isdir(path):
            raise ValueError(f"The path '{path}' is not a directory.")

        self.open_path = path
        return path

    def add_path(self, addition: str):
        new_path = os.path.join(self.open_path, addition)

        if not os.path.exists(new_path):
            raise ValueError(f"The path '{new_path}' does not exist.")
        if not os.path.isdir(new_path):
            raise ValueError(f"The path '{new_path}' is not a directory.")

        self.open_path = new_path
        return new_path

    def get_dirs(self):
        dirs = np.array(os.listdir(self.open_path))
        dirs.sort()
        mask = np.char.startswith(dirs, '.')
        dirs = dirs[~mask]
        return dirs
