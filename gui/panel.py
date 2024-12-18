from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Panel(QWidget):
    def __init__(self, parent, minimum_width=100, minimum_height=100):
        super().__init__(parent)

        self.setMinimumWidth(minimum_width)
        self.setMinimumHeight(minimum_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

