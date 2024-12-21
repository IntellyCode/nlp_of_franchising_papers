from gui.panel import Panel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from .selected_files import SelectedFiles


class RightPanel(Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.sf = SelectedFiles(self)
        self.layout().addWidget(self.sf)

    def add_file(self, item):
        print(item)
        self.sf.add_file(item)
