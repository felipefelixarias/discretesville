from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle

import random
import time


DIMS = [
    (15,17),
    (4,4)
]

img = "../images/logo.png"
pacman = "../images/Pacman.png"
x = "../images/x.png"
qImg = QImage(img)

class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, ville, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y
        self.ville = ville
        self.vertex = self.ville.grid.vertices[x][y]
        self.inPath = False

        #TODO: Enable multiple click start and goal setting by having a flag in ville
        self.isEven = False
        

    def reset(self):
        self.vertex.isGoal = False
        self.vertex.isStart = False
        self.vertex.isStaticObstacle = False
        self.update()

    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.vertex.isStaticObstacle:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        elif self.inPath:
            outer, inner = Qt.gray, Qt.blue
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))

        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.vertex.isStart:
            p.drawPixmap(r, QPixmap(pacman))
        elif self.vertex.isGoal:
            p.drawPixmap(r, QPixmap(x))


    def setStaticObstacle(self):
        self.vertex.isStaticObstacle = not self.vertex.isStaticObstacle
        self.update() 

    def setStartGoal(self):
        if self.ville.robot.task.start is None: 
            self.ville.robot.task.start = self.vertex
            self.vertex.isStart = True
        elif self.ville.robot.task.goal is None:
            self.ville.robot.task.goal = self.vertex
            self.vertex.isGoal = True
       
        self.update()

    def mouseReleaseEvent(self, e):

        # if (e.button() == Qt.RightButton and not self.isStaticObstacle):
        #     self.setStaticObstcale()
        if (e.button() == Qt.RightButton):
            if self.ville.robot.task.start is None or self.ville.robot.task.goal is None:
                self.setStartGoal()
            else:
                obs = DynamicObstacle()
                obs.path.append(self.vertex)
                self.ville.dynamicObstacles.append(obs)


        if (e.button() == Qt.LeftButton):
            if self.ville.robot.task.start is None and self.ville.robot.task.goal is None:
                self.setStaticObstacle()
            else:
                obs = self.ville.dynamicObstacles[-1]
                obs.path.append(self.vertex)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.numRows, self.numCols = DIMS[0]

        self.ville = Discretesville(self.numRows, self.numCols)
        
        w = QWidget()
        hb = QHBoxLayout()

        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon(img))
        self.button.setFlat(True)

        self.button.pressed.connect(self.buttonPressed)

        hb.addWidget(self.button)

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
                w = Pos(x, y, self.ville)
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
            
    def buttonPressed(self):
        if self.ville.robot.task.start is not None and self.ville.robot.task.goal is not None:

            path = self.ville.sssp.dijkstra()
            for i,j in path:
                w = self.grid.itemAtPosition(i,j).widget()
                w.inPath = True
            self.update()
            for obs in self.ville.dynamicObstacles:
                print([o.pos for o in obs.path])

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()