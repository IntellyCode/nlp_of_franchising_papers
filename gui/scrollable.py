from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QPushButton, QLabel


class ScrollableList(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)

        # Main layout for this widget
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Scroll Area to contain the list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setStyleSheet("background-color: white; ")

        # Container widget to hold the list of items
        self.scroll_area_content = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        # Populate the list with selectable items
        for item in items:
            label = Entry(item, self.scroll_area_content)
            self.scroll_layout.addWidget(label)

        self.scroll_area_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        # Add the scroll area to the main layout
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def update(self, items) -> None:
        self.scroll_layout.clear()
        for item in items:
            label = Entry(item, self.scroll_area_content)
            self.scroll_layout.addWidget(label)

class Entry(QLabel):
    def __init__(self, item, parent=None):
        super().__init__(item, parent)
        self.setAlignment(Qt.AlignLeft)
        self.setContentsMargins(6, 2, 3, 2)
        self.setStyleSheet("QLabel { background-color: white; } QLabel:hover { background-color: lightblue; }")
        self.mousePressEvent = lambda event, text=item: self.on_item_selected(text)


    def on_item_selected(self, item):
        print(f"Selected: {item}")
