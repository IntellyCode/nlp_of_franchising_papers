from typing import List
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QPushButton, QLabel
from .entry import Entry


class ScrollableList(QWidget):
    refresh_sgl = pyqtSignal(str)

    def __init__(self, items, parent=None):
        super().__init__(parent)

        self.current_index = 0
        self.entries = []
        self.setMaximumWidth(500)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

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
        self.refresh(items)

        self.scroll_area_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_area_content)

        # Add the scroll area to the main layout
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        if self.entries:
            self.entries[self.current_index].setFocus()
        self.scroll_area.setFocusPolicy(Qt.NoFocus)

    def _clear_layout(self):
        self.current_index = 0
        while self.scroll_layout.count() > 0:
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def refresh(self, items) -> None:
        self._clear_layout()
        self.setFocus()
        self.entries = []
        for item in items:
            label = Label(item, self.scroll_area_content)
            label.setFocusPolicy(Qt.StrongFocus)
            label.clicked.connect(self.refresh_sgl.emit)
            self.scroll_layout.addWidget(label)
            self.entries.append(label)


class Label(Entry):
    clicked = pyqtSignal(str)

    def on_item_selected(self, item):
        self.setFocus()
        self.clicked.emit(item)
