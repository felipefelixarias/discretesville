from vertex import Vertex

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Vertex(False) for _ in range(rows)] for _ in range(cols)]

    def debugPrint(self):
        for row in self.grid:
            t = []
            for v in row:
                if v.occupied:
                    t.append(1)
                else:
                    t.append(0)
            print(t)
        

g = Grid(5,5)
g.debugPrint()
