from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QPushButton, QLabel
from os import sep


class DirectoryTracker(QWidget):
    home = pyqtSignal()
    backward = pyqtSignal()

    def __init__(self, parent, directory):
        super().__init__(parent)

        dir_array = directory.split(sep)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.home_btn = QPushButton("~", self)
        self.home_btn.clicked.connect(self.go_home)

        self.colon = QLabel(":", self)
        self.parent_btn = QPushButton(str(dir_array[-2]), self)
        self.parent_btn.clicked.connect(self.go_backward)

        self.slash = QLabel(str(sep), self)
        self.child_btn = QLabel(str(dir_array[-1]), self)

        layout.addWidget(self.home_btn)
        layout.addWidget(self.colon)
        layout.addWidget(self.parent_btn)
        layout.addWidget(self.slash)
        layout.addWidget(self.child_btn)

    def sizeHint(self):
        return QSize(0, 40)

    def go_home(self):
        self.home.emit()

    def go_backward(self):
        self.backward.emit()

    def refresh(self, directory):
        directory = directory.split(sep)
        self.parent_btn.setText(directory[-2])
        self.child_btn.setText(directory[-1])


