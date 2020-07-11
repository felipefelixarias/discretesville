from json import dump, load
from ville.discretesville import Discretesville
from obstacles.dynamic import DynamicObstacle
from visualize.cell import Cell
import numpy as np
from itertools import combinations
import time



class DCPRM():

    def __init__(self, filename, *args, **kwargs):

        self.filename = filename

        directory_in_str = '../scripts/envGeneration/jsons/'

        with open(directory_in_str+self.filename, 'r') as f:
             self.villeDic = load(f)

        self.numRows, self.numCols = self.villeDic["numRows"], self.villeDic["numCols"]
        self.ville = Discretesville(self.numRows, self.numCols)
        self.loadVille()

        #print("loaded dictionary")
        #print("computing dc")
        self.computeDC()
        time.sleep(2)
        #print("dc computed")
        self.getOccupancyGrids(11)
        time.sleep(2)


    def computeDC(self):

        allVertices = self.ville.grid.sampleVertices(0.2)

        #print("There are " +str(len(allVertices))+" vertices")

        sssps = list(combinations(allVertices, 2))
        #print("Solving " + str(len(sssps)) + " shortest paths")

        for vStart, vGoal in sssps:
            # if iterNumber%500 ==0:
            #     print(iterNumber)

            self.ville.robot.task.start = vStart
            self.ville.robot.task.goal = vGoal

            goal, parent = self.ville.sssp.aStar()
            path = self.ville.sssp.extractPath(goal, parent)
            path.reverse() 

            #print("placing dynamic obstacle")
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

            time.sleep(0.03)

            sipGoal, sipParent = self.ville.sssp.SIPPAStar()

            time.sleep(0.03)


            c = sipGoal
            past = None
            
            while c is not None:
                tempV = self.ville.grid.getVertex(c[0], c[1])
                tempV.touched = True
                if past is not None and ((past[2]-c[2]) > 1):
                    tempV.dynamicCriticality += past[2]-c[2]

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

            time.sleep(0.03)



    def getOccupancyGrids(self, windowSize):
        #print("getting occupancy grid")
        radius = (windowSize-1)//2
        binaryGrid = self.ville.grid.getBinaryArray()
        paddedBinaryGrid = np.pad(binaryGrid, ((radius,radius),(radius, radius)), 'constant', constant_values=((1,1),(1,1)))
        occupancyGrids = []
        dynamicCriticalities = []

        #print(paddedBinaryGrid)
        #print('#'*10)

        for row in range(radius, radius+self.ville.grid.rows):
            for col in range(radius, radius+self.ville.grid.cols):
                if paddedBinaryGrid[row][col] == 0:
                    v = self.ville.grid.getVertex(row-radius, col-radius)
                    if v.touched:
                        dynamicCriticality = v.dynamicCriticality
                        dynamicCriticalities.append(dynamicCriticality)
                        occupancyGrid = paddedBinaryGrid[row-radius:row+radius+1,col-radius:col+radius+1].tolist()
                        occupancyGrids.append(occupancyGrid)

        outDic = {}
        outDic['dc'] = dynamicCriticalities
        outDic['grids'] = occupancyGrids

        out_dir_str = './training/'
        with open(out_dir_str + self.filename, 'w') as fp:
            dump(outDic, fp)

            
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
