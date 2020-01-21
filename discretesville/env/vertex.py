
import sys

class Vertex:
    def __init__(self, isStaticObstacle, pos):
        self.safeIntervals = []
        self.pos = pos
        self.isStaticObstacle = isStaticObstacle
        self.occupied = []
        self.occupiedBy = []
        self.isStart = False
        self.isGoal = False
        self.criticality = 0
        si = self.SafeInterval()
        self.safeIntervals.append(si)

    class SafeInterval:
        def __init__(self):
            self.start = 0
            self.end = sys.maxsize
            self.obsBefore = None
            self.obsAfter = None
            self.index = 0

    def setAsOccupied(self, timestep, obstacle):

        if self.isStaticObstacle:
            self.safeIntervals.clear()

        elif timestep == 0:
            last = self.safeIntervals[-1]
            last.start = timestep + 1
            last.obsBefore = obstacle

        #changed this from if to elif
        elif len(self.safeIntervals) > 0:

            last = self.safeIntervals[-1]

            if last.start == timestep:
                last.start = timestep + 1

            else:
                last = self.safeIntervals[-1]
                last.end = timestep - 1
                last.obsAfter = obstacle

                si = self.SafeInterval()
                si.start = timestep + 1
                si.obsBefore = obstacle
                si.index = last.index + 1

                self.safeIntervals.append(si)

        self.occupied.append(timestep)
        self.occupiedBy.append(obstacle)

    def setAsStaticObstacle(self):
        self.isStaticObstacle = True
        self.safeIntervals.clear()

    def setAsNoObstacle(self):
        self.isStaticObstacle = False
        si = self.SafeInterval()
        self.safeIntervals.append(si)

    def getSafeInterval(self, timestep):
        #TODO: make this faster than linear search
        for si in self.safeIntervals:
            if timestep >= si.start and timestep <= si.end:
                return si

        return None

    def getSafeIntervalByIdx(self,idx):
        if idx >= len(self.safeIntervals) or idx<0:
            print("Invalid index for interval.")
            return None

        return self.safeIntervals[idx]

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return True  


