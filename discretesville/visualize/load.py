from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell

import random
import time
import sys
import json


ville = None

img = "../images/logo.png"
pacman = "../images/Pacman.png"
x = "../images/x.png"
ghost = "../images/ghost.png"
qImg = QImage(img)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.numRows, self.numCols = ville["numRows"], ville["numCols"]
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

        for obs in ville["staticObstacles"]:
            self.ville.grid.getVertex(obs[0],obs[1]).setAsStaticObstacle()

        for dynamicObstacle in ville["dynamicObstacles"]:
            
            path = dynamicObstacle["path"]

            for i, cell in enumerate(path):
                
                v = self.ville.grid.getVertex(cell[0],cell[1])

                if i == 0:
                    obs = DynamicObstacle()
                    obs.path.append(v)
                    self.ville.dynamicObstacles.append(obs)
                    v.setAsOccupied(len(obs.path)-1, obs)
                else:
                    obs = self.ville.dynamicObstacles[-1]
                    obs.path.append(v)
                    v.setAsOccupied(len(obs.path)-1, obs)

        startCell = self.grid.itemAtPosition(ville["robot"]["start"][0],ville["robot"]["start"][1]).widget()
        goalCell = self.grid.itemAtPosition(ville["robot"]["goal"][0],ville["robot"]["goal"][1]).widget()

        startCell.setStartGoal()
        goalCell.setStartGoal()

        self.show()
        self.path = []
        self.timestep = 0

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.numRows):
            for y in range(0, self.numCols):
                w = Cell(x, y, self.ville)
                self.grid.addWidget(w, x, y)
                w.update()
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

            self.path = self.ville.sssp.SIPPAStar()

            for obs in self.ville.dynamicObstacles:
                print([o.pos for o in obs.path])

            timer = QTimer(self)
            timer.timeout.connect(self.updateCell)
            timer.start(500)

            self.ville.robot.task.start = None
            self.ville.robot.task.goal = None
            
        else:
            self.ville.robot.task.start = None
            self.ville.robot.task.goal = None
            self.ville.dynamicObstacles = []
            self.path = []
            self.reset_map()

    #Function that updates the cells at each timestep for animation
    def updateCell(self):

        if (len(self.path) > self.timestep):

            if self.timestep > 0:
                i,j = self.path[self.timestep-1]
                w = self.grid.itemAtPosition(i,j).widget()
                w.inPath = False
                w.update()

                obstaclesPast = [obs.path[self.timestep-1] for obs in self.ville.dynamicObstacles if len(obs.path) > self.timestep -1]

                for o in obstaclesPast:
                    i, j = o.pos
                    w = self.grid.itemAtPosition(i,j).widget()
                    w.isDynamicObstacle = False
                    w.update()

            obstacles = [obs.path[self.timestep] for obs in self.ville.dynamicObstacles if len(obs.path) > self.timestep]

            #i,j = self.path.pop(0)
            for o in obstacles:
                i, j = o.pos
                w = self.grid.itemAtPosition(i,j).widget()
                w.isDynamicObstacle = True
                w.update()

            #print(self.path[self.timestep])
            
            i,j = self.path[self.timestep]
            w = self.grid.itemAtPosition(i,j).widget()
            w.inPath = True
            w.update()         
    
            self.timestep += 1

        
if __name__ == '__main__':
    json_data = sys.argv[1]
    print(json_data)

    with open(json_data, 'r') as f:
        ville = json.load(f)

    print(ville)

    app = QApplication([])

    window = MainWindow()
    
    app.exec_()