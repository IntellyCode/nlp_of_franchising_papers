from typing import LiteralString

from gui.panel import Panel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
import os
from .scrollable import ScrollableList
from .dir_tracker import DirectoryTracker
import numpy as np


class LeftPanel(Panel):
    add_file = pyqtSignal(str)

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.open_path = os.path.expanduser("~")

        self.sl = ScrollableList(self.get_dirs())
        self.sl.refresh_sgl.connect(self.go_forward)

        self.dt = DirectoryTracker(self, self.open_path)
        self.dt.home.connect(self.go_home)
        self.dt.backward.connect(self.go_backward)

        self.layout().addWidget(self.dt)
        self.layout().addWidget(self.sl)

    def set_path(self, path: str | bytes):
        if not os.path.exists(path):
            raise ValueError(f"The path '{path}' does not exist.")
        if not os.path.isdir(path):
            raise ValueError(f"The path '{path}' is not a directory.")

        self.open_path = path
        return path

    def add_path(self, addition: str):
        new_path = os.path.join(self.open_path, addition)

        if not os.path.exists(new_path):
            print(f"Error with: {new_path}")
            return
        if not os.path.isdir(new_path):
            print(f"Error with: {new_path}")
            return

        self.open_path = new_path
        return new_path

    def get_dirs(self):
        dirs = np.array(os.listdir(self.open_path))
        dirs.sort()
        mask = np.char.startswith(dirs, '.')
        dirs = dirs[~mask]

        def check_pdf_dir(item):
            full_path = os.path.join(self.open_path, item)
            return os.path.isdir(full_path) or (os.path.isfile(full_path) and os.path.splitext(full_path)[1].lower() == '.pdf')

        dirs = [dir for dir in dirs if check_pdf_dir(dir)]
        return dirs

    def _refresh(self):
        self.sl.refresh(self.get_dirs())
        self.dt.refresh(self.open_path)

    def go_home(self):
        self.open_path = os.path.expanduser("~")
        self._refresh()

    def go_backward(self):
        dir_list = self.open_path.split(sep=os.sep)
        dir_list.pop(-1)
        if len(dir_list) <= 2:
            self.set_path(os.path.expanduser("~"))
        else:
            self.set_path(f"/{os.path.join(*dir_list)}")
        self._refresh()

    def go_forward(self, item):
        if item.endswith('.pdf'):
            self.add_file.emit(os.path.join(self.open_path, item))
        else:
            self.add_path(item)
            self._refresh()
