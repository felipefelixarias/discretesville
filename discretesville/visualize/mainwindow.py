from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QSize, QTimer

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell

img = "../images/logo.png"

class MainWindow(QMainWindow):
    def __init__(self, villeDic=None, numRows=0, numCols=0, searchAlg="SIPPAStar", *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.villeDic = villeDic
        self.searchAlg = searchAlg

        if self.villeDic is not None:
            self.numRows, self.numCols = self.villeDic["numRows"], self.villeDic["numCols"]
        else:
            self.numRows, self.numCols = numRows,numCols

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

        if self.villeDic is not None:
            self.loadVille()

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

            if self.searchAlg == "SIPPA*":
                self.path = self.ville.sssp.SIPPAStar()
            elif self.searchAlg == "dynamicA*":
                self.path = self.ville.sssp.dynamicAStar()
            elif self.searchAlg == "dijkstra":
                self.path = self.ville.sssp.dijkstra()
            elif self.searchAlg == "A*":
                self.path = self.ville.sssp.aStar()
            else:
                print("Invalid search algorithm, using SIPP A*")
                self.path = self.ville.sssp.SIPPAStar()

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
    
    def printRelevantSafeIntervals(self):
        for dynamicObstacle in ville["dynamicObstacles"]:
            
            path = dynamicObstacle["path"]

            for _, cell in enumerate(path):
                
                v = self.ville.grid.getVertex(cell[0],cell[1])

                print("#"*10)
                print(v.pos)
                for si in v.safeIntervals:
                    print("------")
                    print(si.start)
                    print(si.end)

    def loadVille(self):

        ville = self.villeDic

        for obs in ville["staticObstacles"]:
            self.ville.grid.getVertex(obs[0],obs[1]).setAsStaticObstacle()

        startCell = self.grid.itemAtPosition(ville["robot"]["start"][0],ville["robot"]["start"][1]).widget()
        goalCell = self.grid.itemAtPosition(ville["robot"]["goal"][0],ville["robot"]["goal"][1]).widget()

        startCell.setStartGoal()
        goalCell.setStartGoal()

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
