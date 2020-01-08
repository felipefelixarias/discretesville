from env.vertex import Vertex

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.vertices = [[Vertex(False, (i,j)) for j in range(cols)] for i in range(rows)]

    def debugPrint(self):
        for row in self.grid:
            t = []
            for v in row:
                if v.staticObstacle:
                    t.append(1)
                else:
                    t.append(0)
            print(t)
        

#g = Grid(5,5)
#g.debugPrint()
