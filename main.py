import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from ui.gamehall import *


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())