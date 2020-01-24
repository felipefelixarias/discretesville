from env.grid import Grid
from agent.robot import Robot
from search.sssp import SSSP

class Discretesville:
    """
    Class that encapsulates all aspects of a discrete sssp problem
    
    Parameters
    ----------
    numRows
        The number of rows in the grid.
    numCols
        The number of columns in the grid.

    Attributes
    ----------
    grid
        The grid object that stores all of the vertices.
    robot
        The robot, initialized with no task.
    dynamicObstacles
        A list of dynamicObstacle objects, initially empty.
    sssp
        A single source shortest path object, which can be used for path finding.

    """
    def __init__(self, numRows, numCols):
        self.grid = Grid(numRows, numCols)
        self.robot = Robot()
        self.dynamicObstacles = []
        self.sssp = SSSP(self.grid, self.robot)

        
