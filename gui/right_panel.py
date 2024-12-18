from gui.panel import Panel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class RightPanel(Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        label = QLabel(f"This is a Right Panel")
        label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(label)
