from PyQt5 import QtCore, QtGui, QtWidgets
import os

# Overlay class - A base class for all overlays (task and file)
class Overlay(QtWidgets.QWidget):
    """
    This class serves as a generic overlay, containing a label, a progress bar,
    and a close button. Subclasses like TaskOverlay and FileOverlay can extend
    this base class and customize it for specific use cases, such as tasks or files.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Label for description (e.g., task label or file name)
        self.label = QtWidgets.QLabel(self)
        self.horizontalLayout.addWidget(self.label)

        # Progress bar for task status
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.horizontalLayout.addWidget(self.progress_bar)

        # Close button for task or file removal
        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setMaximumSize(QtCore.QSize(30, 30))
        self.close_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../uis/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_button.setIcon(icon)
        self.horizontalLayout.addWidget(self.close_button)

        self.close_button.clicked.connect(self.close)
    def set_label_text(self, text):
        self.label.setText(text)

    def set_progress(self, value):
        self.progress_bar.setValue(value)


# TaskOverlay class - Specialized overlay for tasks, inherits from Overlay
class TaskOverlay(Overlay):
    """
    A specialized overlay for tasks, inheriting from the Overlay base class.
    It can be used to display task name, progress, and a close button for each task.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumSize(QtCore.QSize(16777215, 40))


# FileOverlay class - Specialized overlay for files, inherits from Overlay
class FileOverlay(Overlay):
    """
    A specialized overlay for files, inheriting from the Overlay base class.
    It can be used to display file names and a progress bar for file-related operations.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Optionally, customize FileOverlay with file-specific behavior
        self.setMinimumSize(QtCore.QSize(0, 40))
        self.setMaximumSize(QtCore.QSize(16777215, 40))


# ControlPanel class for buttons (Start, Clear, Settings)
class ControlPanel(QtWidgets.QWidget):
    """
    This class represents the control panel containing buttons for actions like Start, Clear, and Settings.
    It uses a horizontal layout to place the buttons in a single row.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)

        # Start button
        self.start_button = QtWidgets.QPushButton("Start", self)
        self.horizontalLayout.addWidget(self.start_button)

        # Clear button
        self.clear_button = QtWidgets.QPushButton("Clear", self)
        self.horizontalLayout.addWidget(self.clear_button)

        # Spacer to push buttons to the left
        self.spacer = QtWidgets.QWidget(self)
        self.horizontalLayout.addWidget(self.spacer)

        # Settings button
        self.settings_button = QtWidgets.QPushButton("Settings", self)
        self.horizontalLayout.addWidget(self.settings_button)


class DirectoryViewer(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)

        parent, current = os.path.expanduser("~").split(os.path.sep)[-2:]  # os.getcwd().split(os.path.sep)[-3:-1]
        # Home
        self.home_button = QtWidgets.QPushButton("~", self)
        self.parent_button = QtWidgets.QPushButton(parent, self)
        self.current_button = QtWidgets.QPushButton(current, self)

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setText(":")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setText("/")

        self.horizontalLayout.addWidget(self.home_button)
        self.horizontalLayout.addWidget(self.label_1)
        self.horizontalLayout.addWidget(self.parent_button)
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.current_button)

        self.horizontalLayout.setAlignment(QtCore.Qt.AlignLeft)


# Scrollable panel for directory finder
class ScrollablePanel(QtWidgets.QScrollArea):
    """
    This class creates a scrollable panel. It's used in different sections like directory finder,
    active tasks, or selected files. It allows adding widgets inside it, which can be scrolled vertically.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.scrollable_widget = QtWidgets.QWidget(self)
        self.setWidget(self.scrollable_widget)

        self.scrollable_layout = QtWidgets.QVBoxLayout(self.scrollable_widget)
        self.scrollable_widget.setLayout(self.scrollable_layout)

    def set_content_layout(self, layout):
        self.scrollable_widget.setLayout(layout)


# MainWindow - Assembling all the classes into the main window
class MainWindow(QtWidgets.QWidget):
    """
    This is the main window for the application. It assembles all the components like control panel,
    scrollable panels for active tasks, selected files, and directory finder, into the main layout.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(816, 455)

        # Main layout of the window
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)

        # Left pane with directory finder
        self.left_pane = QtWidgets.QWidget(self)
        self.verticalLayout_left = QtWidgets.QVBoxLayout(self.left_pane)

        self.directory_viewer = DirectoryViewer(self)
        self.verticalLayout_left.addWidget(self.directory_viewer)

        self.directory_finder = ScrollablePanel(self)
        self.directory_finder.setMinimumSize(300, 400)
        self.verticalLayout_left.addWidget(self.directory_finder)

        self.horizontalLayout.addWidget(self.left_pane)

        # Right pane with tasks and selected files
        self.right_pane = QtWidgets.QWidget(self)
        self.verticalLayout_right = QtWidgets.QVBoxLayout(self.right_pane)

        # Active tasks scrollable panel
        self.active_tasks = ScrollablePanel(self)
        self.verticalLayout_right.addWidget(self.active_tasks)

        # Selected files scrollable panel
        self.selected_files = ScrollablePanel(self)
        self.verticalLayout_right.addWidget(self.selected_files)

        self.control_panel = ControlPanel(self)
        self.verticalLayout_right.addWidget(self.control_panel)

        self.horizontalLayout.addWidget(self.right_pane)

        # Initialize overlays
        self.task_overlay1 = TaskOverlay(self)
        self.task_overlay1.set_label_text("Task 1")
        self.task_overlay1.set_progress(50)

        self.task_overlay2 = TaskOverlay(self)
        self.task_overlay2.set_label_text("Task 2")
        self.task_overlay2.set_progress(70)

        self.file_overlay1 = FileOverlay(self)
        self.file_overlay1.set_label_text("File 1")

        self.file_overlay2 = FileOverlay(self)
        self.file_overlay2.set_label_text("File 2")

        # Example of adding overlays to the UI, customize as needed
        self.active_tasks.scrollable_widget.layout().addWidget(self.task_overlay1)
        self.active_tasks.scrollable_widget.layout().addWidget(self.task_overlay2)
        self.selected_files.scrollable_widget.layout().addWidget(self.file_overlay1)
        self.selected_files.scrollable_widget.layout().addWidget(self.file_overlay2)

        self.show()


# Running the application
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec_()
