from env.grid import Grid
from agent.robot import Robot
from search.sssp import SSSP

class Discretesville:
    def __init__(self, numRows, numCols):
        self.grid = Grid(numRows, numCols)
        self.robot = Robot()
        self.dynamicObstacles = []
        self.sssp = SSSP(self.grid, self.robot)

        
