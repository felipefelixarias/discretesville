
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
        #check as soon as timestep is not in occupied
        #may need a flag or a second check for adjacent free timesteps 
        #assume interval will be one unit long, if not edit it dynamically?

        if timestep == 0:
            self.safeIntervals.clear()

        #check if there is already a safe interval
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


    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.distance < other.distance


