from env.grid import Grid

class Discretesville:
    def __init__(self, numRows, numCols):
        self.grid = Grid(numRows, numCols)
        self.robot = None
        self.dynamicObstacles = []
        self.sssp = None

        
    
ville = Discretesville(5,5)
ville.grid.debugPrint()