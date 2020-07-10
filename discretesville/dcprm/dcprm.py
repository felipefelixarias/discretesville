from json import dump
from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell
import numpy as np



class DCPRM():

    def __init__(self, villeDic=None, numRows=0, numCols=0, mode="research", searchAlg="dynamicA*", filename="test", *args, **kwargs):

        self.villeDic = villeDic
        self.searchAlg = searchAlg
        self.mode = mode
        self.filename = filename

        if self.villeDic is not None:
            self.numRows, self.numCols = self.villeDic["numRows"], self.villeDic["numCols"]
        else:
            self.numRows, self.numCols = numRows,numCols

        self.ville = Discretesville(self.numRows, self.numCols)

        if self.villeDic is not None:
            print("loaded dictionary")
            self.loadVille()

        self.buttonPressed()

    def buttonPressed(self):

        if self.mode == "research":

            waitOnly = True

            allVertices = self.ville.grid.getAll()

            # Regular Criticality
            # for v in allVertices:
            #     self.ville.robot.task.start = v
            #     goal, parent = self.ville.sssp.dijkstra()

            #     for key in parent:
            #         path = []
            #         temp = key
            #         while temp is not None:
            #             path.append(temp)
            #             tempV = self.ville.grid.getVertex(temp[0], temp[1])
            #             tempV.criticality += 1
            #             temp = parent[temp]
        

            #maxCriticality = max([v.criticality for v in allVertices])

            for vStart in allVertices:
                self.ville.robot.task.start = vStart
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
                            if not waitOnly:
                                tempV.dynamicCriticality += 1
                        else:
                            #Added this if statement to only count waiting in place
                            if waitOnly:
                                if (past[2]-c[2]) > 1:
                                    for _ in range(past[2]-c[2]):
                                        tempV.dynamicCriticality += 1
                            else:
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
 
            #Normalize?
            #maxDynamicCriticality = max([v.dynamicCriticality for v in allVertices])
            # for v in allVertices:
            #     v.criticality = v.criticality/maxCriticality
            #     v.dynamicCriticality = v.dynamicCriticality/maxDynamicCriticality

    def getOccupancyGrids(self, windowSize):
        radius = (windowSize-1)//2
        binaryGrid = self.ville.grid.getBinaryArray()
        paddedBinaryGrid = np.pad(binaryGrid, ((radius,radius),(radius, radius)), 'constant', constant_values=((1,1),(1,1)))
        occupancyGrids = []
        dynamicCriticalities = []

        print(paddedBinaryGrid)
        print('#'*10)

        for row in range(radius, radius+self.ville.grid.rows):
            for col in range(radius, radius+self.ville.grid.cols):
                if paddedBinaryGrid[row][col] == 0:
                    dynamicCriticality = self.ville.grid.getVertex(row-radius, col-radius).dynamicCriticality
                    dynamicCriticalities.append(dynamicCriticality)
                    occupancyGrid = paddedBinaryGrid[row-radius:row+radius+1,col-radius:col+radius+1]
                    occupancyGrids.append(occupancyGrid)

        for grid, criticality in zip(occupancyGrids, dynamicCriticalities):
            if criticality > 0:
                print(criticality)
                print(grid)

        return paddedBinaryGrid

            
    def loadVille(self):

        ville = self.villeDic

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
