import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QGridLayout


class Pane(QWidget):
    def __init__(self, layout_type='grid', parent=None):
        super().__init__(parent)

        # Set the layout based on the layout_type parameter
        if layout_type == 'grid':
            self.setLayout(QGridLayout())
            # Example: Add some sample labels to the grid
            for i in range(3):
                for j in range(3):
                    label = QLabel(f'Item {i},{j}', self)
                    self.layout().addWidget(label, i, j)
        else:
            # If another layout is needed, you can add it here
            self.setLayout(QVBoxLayout())
            self.layout().addWidget(QLabel('Default layout'), 0)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the fixed size of the window
        self.setFixedSize(800, 600)

        # Create the main layout
        main_layout = QHBoxLayout(self)

        # Create the first pane (left)
        left_pane = Pane(layout_type='default')  # Can be default or any other type
        main_layout.addWidget(left_pane, 1)  # 1 part of width

        # Create the right vertical layout
        right_layout = QVBoxLayout()

        # Create the top right pane (right top)
        right_top_pane = Pane(layout_type='grid')  # This one has grid layout
        right_layout.addWidget(right_top_pane, 1)  # 1 part of height

        # Create the bottom right pane (right bottom)
        right_bottom_pane = Pane(layout_type='default')  # You can change this layout type as needed
        right_layout.addWidget(right_bottom_pane, 1)  # 1 part of height

        main_layout.addLayout(right_layout, 1)  # 1 part of width for right layout

        self.setLayout(main_layout)
        self.setWindowTitle("Flexible Pane Layout")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
