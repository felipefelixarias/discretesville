
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
        self.occupied = []
        self.occupiedBy = []
        self.isStart = False
        self.isGoal = False
        si = self.SafeInterval()
        self.safeIntervals.append(si)

    class SafeInterval:
        def __init__(self):
            self.begin = 0
            self.end = sys.maxsize
            self.obsBefore = None
            self.obsAfter = None

    def setAsOccupied(self, timestep, obstacle):

        if timestep == 0:
            self.safeIntervals.clear()
        elif len(self.safeIntervals) ==  0 and not self.isStaticObstacle:
            si = self.SafeInterval()
            si.begin = timestep + 1
            si.obsBefore = obstacle
            self.safeIntervals.append(si)

        if len(self.safeIntervals) > 0:

            last = self.safeIntervals[-1]

            if last.begin == timestep:
                last.begin = timestep + 1

            else:
                last = self.safeIntervals[-1]
                last.end = timestep - 1
                last.obsAfter = obstacle

                si = self.SafeInterval()
                si.begin = timestep + 1
                si.obsBefore = obstacle

                self.safeIntervals.append(si)

        self.occupied.append(timestep)
        self.occupiedBy.append(obstacle)

    def setAsStaticObstacle(self):
        self.isStaticObstacle = True
        self.safeIntervals.clear()

    def setAsNoObstacle(self):
        self.isStaticObstacle = True
        si = self.SafeInterval()
        self.safeIntervals.append(si)


    def getSafeInterval(self, timestep):
        #could make this faster than linear search

        for si in self.safeIntervals:
            if timestep >= si.begin and timestep <= si.end:
                return si

        return None


    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.distance < other.distance


