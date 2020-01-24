from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import QSize, QTimer
from json import dump

from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell

img = "../images/logo.png"

class MainWindow(QMainWindow):
    def __init__(self, villeDic=None, numRows=0, numCols=0, mode="UX", searchAlg="SIPPA*", filename="test", *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.villeDic = villeDic
        self.searchAlg = searchAlg
        self.mode = mode
        self.filename = filename

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

        if self.mode == "research":

            allVertices = self.ville.grid.getAll()

            for v in allVertices:
                self.ville.robot.task.start = v
                goal, parent = self.ville.sssp.dijkstra()

                for key in parent:
                    path = []
                    temp = key
                    while temp is not None:
                        path.append(temp)
                        tempV = self.ville.grid.getVertex(temp[0], temp[1])
                        tempV.criticality += 1
                        temp = parent[temp]
        

            maxCriticality = max([v.criticality for v in allVertices])

            for vStart in allVertices:
                self.ville.robot.task.start = vStart
                #maybe here will be nested for v in all vertices
                for vGoal in allVertices:
                    if vGoal == vStart:
                        continue 
                    self.ville.robot.task.goal = vGoal

                    goal, parent = self.ville.sssp.dijkstra()
                    path = self.ville.sssp.extractPath(goal, parent)
                    path.reverse() 

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

                    sipGoal, sipParent = self.ville.sssp.SIPPAStar()

                    if sipGoal is None:
                        print("###########")
                        print(vStart.pos)
                        print(vGoal.pos)

                    c = sipGoal
                    past = None

                    while c is not None:
                        tempV = self.ville.grid.getVertex(c[0], c[1])

                        if past is None:
                            tempV.dynamicCriticality += 0
                        else:
                            #Added this if statement to only count waiting in place
                            if (past[2]-c[2]) > 1:
                                for _ in range(past[2]-c[2]):
                                    tempV.dynamicCriticality += 1

                        past = c
                        c = sipParent[c]

                    #RESET

                    for i, cell in enumerate(path):
                    
                        v = self.ville.grid.getVertex(cell[0],cell[1])
                        v.safeIntervals.clear()
                        v.occupied.clear()
                        v.occupiedBy.clear()
                        v.setAsNoObstacle()

                    self.ville.dynamicObstacles.clear()
                    
                    
            maxDynamicCriticality = max([v.dynamicCriticality for v in allVertices])

            for v in allVertices:
                v.criticality = v.criticality/maxCriticality
                v.dynamicCriticality = v.dynamicCriticality/maxDynamicCriticality
                # w = self.grid.itemAtPosition(v.pos[0], v.pos[1]).widget()
                # w.update()

            criticalityDiff = [v.dynamicCriticality - v.criticality for v in allVertices]
            maxDiff = max(criticalityDiff)
            minDiff = min(criticalityDiff)

            for v in allVertices:
                x = v.dynamicCriticality - v.criticality
                #v.criticality = (x - minDiff)/(maxDiff - minDiff)
                #v.criticality = v.criticality
                v.criticality = v.dynamicCriticality
                w = self.grid.itemAtPosition(v.pos[0], v.pos[1]).widget()
                w.update()

            self.ville.grid.printCriticality()

            

        elif self.mode == "save":
            #TODO: Check if user has given robot a start and goal

            ville = {"numRows" : self.ville.grid.rows,
                    "numCols" : self.ville.grid.cols,
                    "robot" : {"start":list(self.ville.robot.task.start.pos), "goal":list(self.ville.robot.task.goal.pos)},
                    "staticObstacles" : [list(o.pos) for o in self.ville.grid.getAllStaticObs()],
                    "dynamicObstacles" : [[list(v.pos) for v in obs.path] for obs in self.ville.dynamicObstacles]}

            with open(self.filename, 'w') as fp:
                dump(ville, fp)
        
        elif self.ville.robot.task.start is not None and self.ville.robot.task.goal is not None:

            if self.searchAlg == "SIPPA*":
                goal, parent = self.ville.sssp.SIPPAStar()
                if goal is None:
                    self.path = []
                else:
                    self.path = self.ville.sssp.extractSIPPPath(goal, parent)

            elif self.searchAlg == "dynamicA*":
                self.path = self.ville.sssp.dynamicAStar()
            elif self.searchAlg == "dijkstra":
                goal, parent = self.ville.sssp.dijkstra()
                if goal is None:
                    self.path = []
                else:
                    self.path = self.ville.sssp.extractPath(goal, parent)

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
            #TODO either delete this, or enable reset
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
    
    def loadVille(self):

        ville = self.villeDic

        for obs in ville["staticObstacles"]:
            self.ville.grid.getVertex(obs[0],obs[1]).setAsStaticObstacle()

        startCell = self.grid.itemAtPosition(ville["robot"]["start"][0],ville["robot"]["start"][1]).widget()
        goalCell = self.grid.itemAtPosition(ville["robot"]["goal"][0],ville["robot"]["goal"][1]).widget()

        startCell.setStartGoal()
        goalCell.setStartGoal()

        for dynamicObstacle in ville["dynamicObstacles"]:
            print("Setting dynamic obstacle..")
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
