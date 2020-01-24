from env.vertex import Vertex

class Grid:
    """ Data structure that stores all of the vertices in a multi-dimensional list.
        
    Parameters
    ----------
    rows
        The number of rows in the grid.
    cols
        The number of columns in the grid.
  
    Attributes
    ----------
    rows
        The number of rows in the grid.
    cols
        The number of columns in the grid.
    vertices
        A two-dimensional list that stores the vertices.
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.vertices = [[Vertex(False, (i,j)) for j in range(cols)] for i in range(rows)]


    def getNeighbors(self, vertex):
        """ Get neighbors of vertex that are not static obstacles.
    
        Parameters
        ----------
        vertex
            The vertex whose neighbors should be returned.

        Returns
        ----------
        neighbors
            A list of vertex objects which are neighbors of the requested vertex.
        """
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

    #Get all unvisited vertices that are not static obstacles
    def getAll(self):
        """Get all vertices that are not static obstacles.
    
  
        Returns
        ----------
        nonObstacles
            A list of all vertices that are not static obstacles.

        """
        nonObstacles = []
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.vertices[i][j].isStaticObstacle:

                    nonObstacles.append(self.vertices[i][j])
        return nonObstacles

    def getAllStaticObs(self):
        out = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.vertices[i][j].isStaticObstacle:
                    out.append(self.vertices[i][j])
        return out
    
    def getVertex(self, x, y):
        return self.vertices[x][y]

    def printCriticality(self):
        for row in self.vertices:
            t = []
            for v in row:
                t.append(v.dynamicCriticality)
            print(t)