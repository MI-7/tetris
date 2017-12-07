from PyQt5.QtWidgets import QGridLayout, QPushButton
from gamesocket.gameclient import *
from ui.TetrisWindow import *


class GameWindow(QMainWindow):
    def __init__(self, mainuser, opponent, roomname):
        super().__init__()
        self.mainuser = mainuser
        self.opponent = opponent
        self.roomname = roomname

        self.is_mainuser = False
        self.is_opponent = False

        if self.mainuser != '':
            tlog(MDEBUG, 'joined as main user')
            self.is_mainuser = True

        if self.opponent != '':
            tlog(MDEBUG, 'joined as opponent')
            self.is_opponent = True

        self.initUI()

        self.query_opponent_timer = QBasicTimer()
        self.query_interval = 1000
        self.query_opponent_timer.start(self.query_interval, self)

    def timerEvent(self, event):
        '''handles timer event'''

        print('timer event')
        if event.timerId() == self.query_opponent_timer.timerId():
            print('query timer event')
            if self.is_mainuser:
                self.opponent = queryopponent(self.roomname)
                print(self.opponent)
                if self.opponent != '':
                    tlog(MDEBUG, 'opponent joined, stop timer')
                    print('found opponent:', self.opponent)
                    self.query_opponent_timer.stop()

            if self.is_opponent:
                tlog(MDEBUG, 'joined as opponent, stop timer')
                self.query_opponent_timer.stop()
        else:
            super(GameWindow, self).timerEvent(event)

    def test_action(self):
        print('test ')

        # self.opboard.tryMove(self.opboard.curPiece.rotateLeft(), self.opboard.curX, self.opboard.curY)
        self.opboard.tryMove(self.opboard.curPiece, self.opboard.curX - 1, self.opboard.curY)

    def initUI(self):
        '''initiates application UI'''

        self.myboard = TetrisBoard(self)
        self.opboard = TetrisBoard(self)
        # self.setCentralWidget(self.tboard)

        # self.statusbar = self.statusBar()
        # self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # self.myboard.start()
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
