#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This is a Tetris game clone.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017

New Author: Leon Chan
leonchan1204@hotmail.com
"""

from PyQt5.QtWidgets import QFrame, QDesktopWidget, QApplication, QWidget, QMainWindow
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys, random


class TetrisBoard(QFrame):
    msg2Statusbar = pyqtSignal(str)
    outofshape_signal = pyqtSignal()

    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    KeyMap = {Qt.Key_Left: 0,
              Qt.Key_Right: 1,
              Qt.Key_Up: 2,
              Qt.Key_Down: 3,
              Qt.Key_Space: 4}

    def __init__(self, parent, is_main_board):
        super().__init__(parent)
        self.is_main_board = is_main_board

        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

        self.shapes = []  # self.generate_random_shapes()
        self.backup_shapes = []

        self.key_sequence = []

    def generate_random_shapes(self):
        shapes = [Shape() for i in range(100)]
        [shape.setRandomShape() for shape in shapes]
        return shapes

    def shapeAt(self, x, y):
        '''determines shape at the board position'''

        return self.board[(y * TetrisBoard.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        '''sets a shape at the board'''

        self.board[(y * TetrisBoard.BoardWidth) + x] = shape

    def squareWidth(self):
        '''returns the width of one square'''

        return self.contentsRect().width() // TetrisBoard.BoardWidth

    def squareHeight(self):
        '''returns the height of one square'''

        return self.contentsRect().height() // TetrisBoard.BoardHeight

    def start(self):
        '''starts game'''

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        # self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(TetrisBoard.Speed, self)

    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(TetrisBoard.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()

    def paintEvent(self, event):
        '''paints all shapes of the game'''

        if not self.isStarted:
            return

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - TetrisBoard.BoardHeight * self.squareHeight()

        for i in range(TetrisBoard.BoardHeight):
            for j in range(TetrisBoard.BoardWidth):
                shape = self.shapeAt(j, TetrisBoard.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (TetrisBoard.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def timerEvent(self, event):
        '''handles timer event'''

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()

        else:
            super(TetrisBoard, self).timerEvent(event)

    def clearBoard(self):
        '''clears shapes from the board'''

        for i in range(TetrisBoard.BoardHeight * TetrisBoard.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def dropDown(self):
        '''drops down a shape'''

        newY = self.curY

        while newY > 0:

            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break

            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        '''goes one line down with a shape'''

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        '''after dropping shape, remove full lines and create new shape'''

        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        '''removes all full lines from the board'''

        numFullLines = 0
        rowsToRemove = []

        for i in range(TetrisBoard.BoardHeight):

            n = 0
            for j in range(TetrisBoard.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, TetrisBoard.BoardHeight):
                for l in range(TetrisBoard.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()

    def newPiece(self):
        '''creates a new shape'''

        if len(self.shapes) == 0:
            print('no shapes')
            self.shapes = self.backup_shapes

        self.curPiece = self.shapes[0]
        self.shapes.remove(self.curPiece)

        if len(self.shapes) == 10:
            if self.is_main_board:
                self.backup_shapes = self.generate_random_shapes()
                self.outofshape_signal.emit()

        self.curX = TetrisBoard.BoardWidth // 2 + 1
        self.curY = TetrisBoard.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.msg2Statusbar.emit("Game over")

    def tryMove(self, newPiece, newX, newY):
        '''tries to move a shape'''

        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= TetrisBoard.BoardWidth or y < 0 or y >= TetrisBoard.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def drawSquare(self, painter, x, y, shape):
        '''draws a square of a shape'''

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)



class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)

    def shape(self):
        '''returns shape'''

        return self.pieceShape

    def setShape(self, shape):
        '''sets a shape'''

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        '''chooses a random shape'''

        self.setShape(random.randint(1, 7))

    def x(self, index):
        '''returns x coordinate'''

        return self.coords[index][0]

    def y(self, index):
        '''returns y coordinate'''

        return self.coords[index][1]

    def setX(self, index, x):
        '''sets x coordinate'''

        self.coords[index][0] = x

    def setY(self, index, y):
        '''sets y coordinate'''

        self.coords[index][1] = y

    def minX(self):
        '''returns min x value'''

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        '''returns max x value'''

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        '''returns min y value'''

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        '''returns max y value'''

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotateLeft(self):
        '''rotates shape to the left'''

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotateRight(self):
        '''rotates shape to the right'''

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


