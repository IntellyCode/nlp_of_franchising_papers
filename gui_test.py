from PyQt5 import QtWidgets

from gui.start_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationName("Abstractor")
    app.setApplicationDisplayName("Abstractor")
    window = MainWindow()
    app.exec_()
