
import sys

class Vertex:
    """
    Class in charge of all single source shortest path algorithms
    
    Parameters
    ----------
    isStaticObstacle
        Boolean which determines if vertex is a static obstacle.
    pos
        Tuple of indices corresponding to the row and column position of vertex in the grid.

    Attributes
    ----------
    safeIntervals
        Array of safe intervals for vertex (defaults to 1 if no dynamic obstacle).
    pos
        Tuple of indices corresponding to the row and column position of vertex in the grid.
    isStaticObstacle
        Boolean which determines if vertex is a static obstacle.
    occupied
        Array of time steps during which vertex is occupied by a dynamic obstacle.
    occupiedBy
        Array of dynamic obstacle objects that correspond to the time steps in occupied.
    isStart
        Boolean which determines if the vertex is the start of a robot.
    isGoal
        Boolean which determines if the vertex is the goal of a robot.
    criticality
        Integer used to keep track of criticality.
    dynamicCriticality
        Integer used to keep track of dynamic criticality.

    """
    def __init__(self, isStaticObstacle, pos):

        self.safeIntervals = []
        self.pos = pos
        self.isStaticObstacle = isStaticObstacle
        self.occupied = []
        self.occupiedBy = []
        self.isStart = False
        self.isGoal = False
        self.criticality = 0
        self.dynamicCriticality = 0
        si = self.SafeInterval()
        self.safeIntervals.append(si)

    class SafeInterval:
        """
        Class storing information for a safe interval

        Attributes
        ----------
        start
            The time step at which the safe interval starts.
        end
            The time step at which the safe interval ends.
        obsBefore
            The obstacle before the safe interval.
        obsAfter
            The obstacle after the safe interval.
        index
            Index of the safe interval.

        """
        def __init__(self):
            self.start = 0
            self.end = sys.maxsize
            self.obsBefore = None
            self.obsAfter = None
            self.index = 0

    def setAsOccupied(self, timestep, obstacle):
        """
        Function used to update a vertex when a dynamic obstacle goes through it.
        
        Parameters
        ----------
        timestep
            Timestep at which the robot is being occupied.
        obstacle
            Dynamic obstacle object that is occupying the vertex.

        """

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
        """
        Function used set vertex as a static obstacle.

        """
        self.isStaticObstacle = True
        self.safeIntervals.clear()

    def setAsNoObstacle(self):
        """
        Function used set vertex as not a static obstacle.

        """
        self.isStaticObstacle = False
        si = self.SafeInterval()
        self.safeIntervals.append(si)

    def getSafeInterval(self, timestep):
        """
        Function used to get safe interval corresponding to a specific timestep.
        
        Parameters
        ----------
        timestep
            The timestep that is within the desired safe interval.
        Returns
        ----------
        si 
            The safe interval object that contains the requested timestep.

        """
        #TODO: make this faster than linear search
        for si in self.safeIntervals:
            if timestep >= si.start and timestep <= si.end:
                return si


        print("No valid safe interval at", timestep)
        return None

    def getSafeIntervalByIdx(self,idx):
        """
        Function used to get safe interval by its index in chronological order.
        
        Parameters
        ----------
        idx
            The index of the requested safe interval.
        Returns
        ----------
        self.safeIntervals[idx]
            The safe interval object that contains the requested timestep.

        """
        if idx >= len(self.safeIntervals) or idx<0:
            print("Invalid index for interval.")
            return None

        return self.safeIntervals[idx]

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return True  


