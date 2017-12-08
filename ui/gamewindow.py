from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtWidgets import QGridLayout, QPushButton, QLabel
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

        self.count_down = 3

        self.query_opponent_timer = QBasicTimer()
        self.query_interval = 1000
        self.query_opponent_timer.start(self.query_interval, self)

        self.gamestart_timer = QBasicTimer()
        self.gamestart_jump = 1000

        self.query_gamestart_timer = QBasicTimer()
        self.query_gamestart_interval = 1000

        if self.is_opponent:
            self.query_gamestart_timer.start(self.query_gamestart_interval, self)

        self.query_shape_timer = QBasicTimer()
        self.query_shape_interval = 1000

    def convert_shape_into_sequence(self, shapes):
        seq = ''.join([str(shape.pieceShape) for shape in shapes])
        print(self.is_mainuser, self.is_opponent, seq)
        return seq


    def convert_sequence_into_shapes(self, sequence):
        ss = [Shape() for s in sequence]
        [shape.setShape(int(seq)) for (shape, seq) in zip(ss, sequence)]
        return ss


    def timerEvent(self, event):
        '''handles timer event'''

        if event.timerId() == self.query_opponent_timer.timerId():
            print('query timer event')
            if self.is_mainuser:
                self.opponent = queryopponent(self.roomname)
                print(self.opponent)
                if self.opponent != '':
                    tlog(MDEBUG, 'opponent joined, stop timer')
                    print('found opponent:', self.opponent)
                    self.query_opponent_timer.stop()
                    self.btn_gamestart.setEnabled(True)

            if self.is_opponent:
                self.mainuser = querymainuser(self.roomname)
                if self.mainuser != '':
                    tlog(MDEBUG, 'joined as opponent, stop timer')
                    print('found mainuser:', self.mainuser)
                    self.query_opponent_timer.stop()
        elif event.timerId() == self.gamestart_timer.timerId():
            self.lbl_countdown.setText(str(self.count_down))
            self.count_down = self.count_down - 1

            if len(self.myboard.shapes) == 0:
                self.myboard.shapes = self.myboard.generate_random_shapes()

                if self.is_mainuser:
                    submitshapes(self.mainuser, self.convert_shape_into_sequence(self.myboard.shapes))

                if self.is_opponent:
                    submitshapes(self.opponent, self.convert_shape_into_sequence(self.myboard.shapes))

            if self.count_down == 2:
                self.query_shape_timer.start(self.query_shape_interval, self)

            if self.count_down == 0:
                self.count_down = 3
                self.lbl_countdown.setText("Go!")
                self.gamestart_timer.stop()

                self.myboard.start()
                self.opboard.start()
        elif event.timerId() == self.query_gamestart_timer.timerId():
            response = querygamestart(self.roomname)
            print('timer, ', '.', response, '.')
            if response == 1:
                self.query_gamestart_timer.stop()
                self.gamestart_timer.start(self.gamestart_jump, self)
        elif event.timerId() == self.query_shape_timer.timerId():
            if self.is_mainuser:
                sequence = getshapes(self.opponent)
                if sequence != '':
                    print('main..', sequence)
                    ss = self.convert_sequence_into_shapes(sequence)
                    self.opboard.backup_shapes = ss

            if self.is_opponent:
                sequence = getshapes(self.mainuser)
                if sequence != '':
                    print('oppo..', sequence)
                    ss = self.convert_sequence_into_shapes(sequence)
                    self.opboard.backup_shapes = ss
        else:
            super(GameWindow, self).timerEvent(event)

    def test_action(self):
        print('test ')

        # self.opboard.tryMove(self.opboard.curPiece.rotateLeft(), self.opboard.curX, self.opboard.curY)
        self.opboard.tryMove(self.opboard.curPiece, self.opboard.curX - 1, self.opboard.curY)

    def game_start(self):
        self.gamestart_timer.start(self.gamestart_jump, self)
        gamestart(self.roomname)

    def outofshape(self):
        sequence = self.convert_shape_into_sequence(self.myboard.backup_shapes)
        if self.is_mainuser:
            submitshapes(self.mainuser, sequence)
            print('..', self.mainuser, sequence)

        if self.is_opponent:
            submitshapes(self.opponent, sequence)
            print('..', self.opponent, sequence)

    def initUI(self):
        '''initiates application UI'''

        self.myboard = TetrisBoard(self, True)
        self.opboard = TetrisBoard(self, False)

        self.myboard.outofshape_signal.connect(self.outofshape)

        # self.statusbar = self.statusBar()
        # self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # self.myboard.start()
        # self.opboard.start()

        self.btn_test = QPushButton("Test")
        self.btn_test.clicked.connect(self.test_action)

        self.lbl_countdown = QLabel('x')
        self.lbl_countdown.setAlignment(Qt.AlignCenter)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.lbl_countdown.setAutoFillBackground(True)
        self.lbl_countdown.setPalette(pe)
        self.lbl_countdown.setFont(QFont("Roman times", 20, QFont.Bold))

        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('Tetris')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.myboard, 0, 0)
        grid.addWidget(self.lbl_countdown, 0, 1)
        grid.addWidget(self.opboard, 0, 2)

        if self.is_mainuser:
            self.btn_gamestart = QPushButton("Game Start")
            self.btn_gamestart.clicked.connect(self.game_start)
            self.btn_gamestart.setEnabled(False)
            grid.addWidget(self.btn_gamestart, 1, 1)

        displaywidget = QWidget()
        displaywidget.setLayout(grid)
        self.setCentralWidget(displaywidget)


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
