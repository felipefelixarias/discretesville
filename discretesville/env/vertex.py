
class Vertex:
    def __init__(self, occupied, pos):
        self.occupied = occupied
        self.safeIntervals = []
        self.pos = pos
        self.staticObstacle = occupied
