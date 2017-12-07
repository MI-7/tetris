from PyQt5.QtWidgets import QGridLayout, QPushButton

from ui.TetrisWindow import *


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def test_action(self):
        print('test ')
        for i in range(100):
            self.opboard.handleKeyPress(Qt.Key_Up)

    def initUI(self):
        '''initiates application UI'''

        self.myboard = TetrisBoard(self)
        self.opboard = TetrisBoard(self)
        # self.setCentralWidget(self.tboard)

        # self.statusbar = self.statusBar()
        # self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.myboard.start()
        self.opboard.start()

        self.btn_test = QPushButton("Test")
        self.btn_test.clicked.connect(self.test_action)

        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('Tetris')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.myboard, 0, 0)
        grid.addWidget(self.opboard, 0, 1)

        grid.addWidget(self.btn_test, 1, 0)

        displaywidget = QWidget()
        displaywidget.setLayout(grid)
        self.setCentralWidget(displaywidget)
        print(5)

    def center(self):
        '''centers the window on the screen'''

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication([])
    win = GameWindow()
    win.show()
    sys.exit(app.exec_())