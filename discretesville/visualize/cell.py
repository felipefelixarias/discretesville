from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle

import random
import time
import sys
import json

img = "../images/logo.png"
pacman = "../images/Pacman.png"
x = "../images/x.png"
ghost = "../images/ghost.png"
qImg = QImage(img)

class Cell(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, ville, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

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
        self.inPath = False
        self.isDynamicObstacle = False
        self.vertex.occupied = []
        self.vertex.occupiedBy = []
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
        elif self.isDynamicObstacle:
            outer, inner = Qt.gray, Qt.red
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))

        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.inPath:
            p.drawPixmap(r, QPixmap(pacman))

        if self.isDynamicObstacle:
            p.drawPixmap(r, QPixmap(ghost))

        if self.vertex.isStart:
            p.drawPixmap(r, QPixmap(pacman))
            self.vertex.isStart = False
        if self.vertex.isGoal:
            p.drawPixmap(r, QPixmap(x))


    def setStaticObstacle(self):
        if self.vertex.isStaticObstacle:
            self.vertex.setAsNoObstacle()
        else:
            self.vertex.setAsStaticObstacle()
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

        if (e.button() == Qt.RightButton):
            if self.ville.robot.task.start is None or self.ville.robot.task.goal is None:
                self.setStartGoal()
            else:
                obs = DynamicObstacle()
                obs.path.append(self.vertex)
                self.ville.dynamicObstacles.append(obs)
                self.vertex.setAsOccupied(len(obs.path)-1, obs)

        if (e.button() == Qt.LeftButton):
            if self.ville.robot.task.start is None and self.ville.robot.task.goal is None:
                self.setStaticObstacle()
            else:
                obs = self.ville.dynamicObstacles[-1]
                obs.path.append(self.vertex)
                self.vertex.setAsOccupied(len(obs.path)-1, obs)

    
