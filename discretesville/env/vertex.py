
import sys

class Vertex:
    def __init__(self, isStaticObstacle, pos):
        #helper variables for dijkstra
        self.visited = False
        self.previous = None
        self.distance = sys.maxsize


        self.safeIntervals = []
        self.pos = pos
        self.isStaticObstacle = isStaticObstacle
        self.isStart = False
        self.isGoal = False

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.distance < other.distance

