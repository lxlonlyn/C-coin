from PyQt5.QtWidgets import QApplication
from GUI.MainWidget import MainWindow
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())