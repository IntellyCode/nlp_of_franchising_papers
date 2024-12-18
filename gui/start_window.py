from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QMessageBox
from gui import RightPanel, LeftPanel


class MainWindow(QtWidgets.QMainWindow):
    """
    This is the main window for the application. It assembles all the components like control panel,
    scrollable panels for active tasks, selected files, and directory finder, into the main layout.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abstractor")
        self.resize(816, 455)

        # Set up left and right panels
        self.left_panel = LeftPanel(self)
        self.left_panel.setMinimumSize(300, 400)

        self.right_panel = RightPanel(self)
        self.right_panel.setMinimumSize(300, 400)

        # Create central widget with horizontal layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        horizontal_layout = QtWidgets.QHBoxLayout(central_widget)
        horizontal_layout.addWidget(self.left_panel)
        horizontal_layout.addWidget(self.right_panel)

        self.show()

    def open_settings(self):
        """Open a simple Settings dialog."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Settings")
        msg.setText("Settings window placeholder")
        msg.exec_()

