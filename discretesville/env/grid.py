from env.vertex import Vertex

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.vertices = [[Vertex(False, (i,j)) for j in range(cols)] for i in range(rows)]

    def debugPrint(self):
        for row in self.vertices:
            t = []
            for v in row:
                if v.staticObstacle:
                    t.append(1)
                else:
                    t.append(0)
            print(t)

    def getNeighbors(self, vertex):
        row, col = vertex.pos
        neighbors = []
        if row < self.rows - 1 and not self.vertices[row+1][col].isStaticObstacle:
            neighbors.append(self.vertices[row+1][col])
        if row > 0 and not self.vertices[row-1][col].isStaticObstacle:
            neighbors.append(self.vertices[row-1][col])
        if col < self.cols - 1 and not self.vertices[row][col+1].isStaticObstacle:
            neighbors.append(self.vertices[row][col+1])
        if col > 0 and not self.vertices[row][col-1].isStaticObstacle:
            neighbors.append(self.vertices[row][col-1])

        return neighbors

    #Get all unvisited vertices that are not static obstacles or have been visited
    def getAll(self):
        out = []
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.vertices[i][j].isStaticObstacle and not self.vertices[i][j].visited:
                    out.append(self.vertices[i][j])
        return out
    
    def getVertex(self, x, y):
        return self.vertices[x][y]