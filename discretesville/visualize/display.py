from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ville.discretesville import Discretesville

import random
import time


DIMS = [
    (3,7),
    (4,4)
]

img = "../images/logo.png"
qImg = QImage(img)

class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, vertex, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y
        self.vertex = vertex

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.is_static_obstacle = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_static_obstacle:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        # if self.is_revealed:
        #     if self.is_start:
        #         p.drawPixmap(r, QPixmap(img))

        #     elif self.is_mine:
        #         p.drawPixmap(r, QPixmap(img))

        #     elif self.adjacent_n > 0:
        #         pen = QPen(NUM_COLORS[self.adjacent_n])
        #         p.setPen(pen)
        #         f = p.font()
        #         f.setBold(True)
        #         p.setFont(f)
        #         p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

        # elif self.is_flagged:
        #     p.drawPixmap(r, QPixmap(img))

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def setStaticObstacle(self):
        self.is_static_obstacle =  not self.is_static_obstacle
        self.vertex.staticObstacle = self.is_static_obstacle
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):

        # if (e.button() == Qt.RightButton and not self.is_static_obstacle):
        #     self.setStaticObstcale()

        if (e.button() == Qt.LeftButton):
            self.setStaticObstacle()

            # if self.is_mine:
            #     self.ohno.emit()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.numRows, self.numCols = DIMS[0]

        self.ville = Discretesville(self.numRows, self.numCols)
        
        w = QWidget()
        hb = QHBoxLayout()

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        
        self.mines.setFont(f)
        self.clock.setFont(f)

        self.mines.setText("000")
        self.clock.setText("000")

        self.robot = QPushButton

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon(img))
        self.button.setFlat(True)

        #self.button.pressed.connect(self.button_pressed)

        # l = QLabel()
        # l.setPixmap(QPixmap.fromImage(qImg))
        # l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # hb.addWidget(l)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        # l = QLabel()
        # l.setPixmap(QPixmap.fromImage(qImg))
        # l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # hb.addWidget(l)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)

        self.setCentralWidget(w)

        self.init_map()
        self.reset_map()

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.numRows):
            for y in range(0, self.numCols):
                w = Pos(x, y, self.ville.grid.vertices[x][y])
                self.grid.addWidget(w, x, y)
                # Connect signal to handle expansion.
                #w.clicked.connect(self.trigger_start)
                #w.expandable.connect(self.expand_reveal)
                #w.ohno.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.numRows):
            for y in range(0, self.numCols):
                w = self.grid.itemAtPosition(x, y).widget()
                w.reset()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()