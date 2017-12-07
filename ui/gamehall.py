from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QPushButton, QListWidget, QLineEdit, QWidget
from gamesocket.gameclient import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()


    def create_room(self):
        uname = self.text_user.text()
        roomname = self.text_room.text()
        response = createroom(roomname, uname)
        # don't refresh, just go to next window
        # self.refresh_room()
        if response == SERVER_RESPONSE_SUCCESS:
            print("yeah")


    def refresh_room(self):
        rooms = listroom()
        print(rooms)

        self.lst_rooms.clear()

        for room in rooms:
            self.lst_rooms.addItem(room)


    def join_room(self):
        # roomname = self.lst_rooms.selection
        pass


    def initUI(self):
        self.resize(640, 480)
        # self.center()
        self.setWindowTitle('Tetris')

        self.lbl_user = QLabel('uname')
        self.text_user = QLineEdit()
        self.lbl_room = QLabel('room')
        self.text_room = QLineEdit()
        self.btn_create_room = QPushButton('Create Room')
        self.btn_create_room.clicked.connect(self.create_room)
        self.lst_rooms = QListWidget()
        self.btn_refresh_rooms = QPushButton('Refresh')
        self.btn_refresh_rooms.clicked.connect(self.refresh_room)
        self.btn_join_room = QPushButton('Join Room')
        self.btn_join_room.clicked.connect(self.join_room)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.lbl_user, 0, 0)
        grid.addWidget(self.text_user, 0, 1, 1, 2)

        grid.addWidget(self.lbl_room, 1, 0)
        grid.addWidget(self.text_room, 1, 1, 1, 2)

        grid.addWidget(self.btn_create_room, 2, 1)

        grid.addWidget(self.lst_rooms, 3, 0, 3, 3)

        grid.addWidget(self.btn_refresh_rooms, 6, 0)
        grid.addWidget(self.btn_join_room, 6, 1)

        displaywidget = QWidget()
        displaywidget.setLayout(grid)
        self.setCentralWidget(displaywidget)

        self.show()