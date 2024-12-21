import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .entry import Entry
from os import sep


class SelectedFiles(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(200, 200)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.files = []
        self.entries = []
        self._refresh()

    def _refresh(self):
        self.entries = []
        for file in self.files:
            entry = FileEntry(file, self)
            self.entries.append(entry)

    def add_file(self, file_path):
        if os.path.isfile(file_path):
            self.files.append(file_path)
        else:
            print("Error in adding file")
        self._refresh()


class FileEntry(Entry):
    def on_item_selected(self, item: str):
        self.setFocus()

