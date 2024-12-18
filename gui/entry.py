from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel


class Entry(QLabel):
    def __init__(self, item, parent=None):
        super().__init__(item, parent)
        self.setAlignment(Qt.AlignLeft)
        self.setContentsMargins(6, 2, 3, 2)
        self.setStyleSheet("""
            QLabel { 
                background-color: white; 
            } 
            QLabel:hover { 
                background-color: lightblue; 
            }
        """)
        self.mousePressEvent = lambda event: self.setFocus()

    def focusInEvent(self, event):
        self.setStyleSheet("""
            QLabel { 
                background-color: lightgray; 
            } 
        """)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet("""
            QLabel { 
                background-color: white; 
            } 
            QLabel:hover { 
                background-color: lightblue; 
            }
        """)
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.on_item_selected(self.text())
        else:
            super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.on_item_selected(self.text())
        super().mouseDoubleClickEvent(event)

    def on_item_selected(self, item: str):
        pass
